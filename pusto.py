#!/usr/bin/env python
import argparse
import datetime as dt
import http.client
import http.server
import json
import os
import pickle
import re
import shutil
import subprocess
import time
from collections import namedtuple, OrderedDict
from threading import Thread
from urllib.error import HTTPError
from urllib.parse import urljoin

from jinja2 import Environment, FileSystemLoader
from lxml import etree
from pytz import timezone, utc


ROOT_DIR = os.getcwd()
SRC_DIR = ROOT_DIR + '/data'
BUILD_DIR = ROOT_DIR + '/build'
CACHE_FILE = '.cache'
URLS_FILE = 'urls.json'
META_FILE = 'meta.json'
INDEX_FILES = ['index.' + t for t in 'py tpl rst md html'.split(' ')]


class Page:
    __slots__ = ('_data',)
    meta_fields = (
        'template params aliases published sort archive author title '
        'terms_file'.split()
    )
    fields = meta_fields + (
        'pages url src_dir index_file meta_file summary body text'.split()
    )
    Data = namedtuple('Data', fields)

    def __init__(self, data):
        defaults = {'sort': '', 'params': {}, 'terms_file': '/terms.html'}
        for key in self.fields:
            data.setdefault(key, defaults.get(key))

        self._data = self.Data(**data)

    def __getattr__(self, key):
        if key in self._data._fields:
            return getattr(self._data, key)

    def __str__(self):
        return '<Page "%s">' % self.url

    def __repr__(self):
        return str(self)

    def get(self, key=None):
        if not key:
            return self._data._asdict()
        return getattr(self._data, key)

    def update(self, **kw):
        self._data = self._data._replace(**kw)

    def src(self, file):
        assert file in ['meta_file', 'index_file']
        return self.src_dir + getattr(self, file)

    def get_meta(self):
        with open(self.src_dir + self.meta_file, 'br') as f:
            raw = json.loads(f.read().decode())

        meta = {}
        for key in Page.meta_fields:
            if key in raw:
                meta[key] = raw[key]

        pub = ''
        if 'published' in meta:
            pub = dt.datetime.strptime(meta['published'], '%Y-%m-%d %H:%M')
            pub = pub.replace(hour=8)
            pub = get_globals(self.src_dir, 'tz').localize(pub)
            meta['published'] = pub

        if 'sort' not in meta:
            meta['sort'] = pub and pub.isoformat()

        if 'terms_file' in meta:
            meta['terms_file'] = '/' + meta['terms_file'].lstrip('/')
        return meta

    @property
    def type(self):
        return self.index_file and self.index_file.rsplit('.', 1)[1]

    @property
    def path(self):
        path = self.src_dir + self.url
        if not self.url.endswith('/'):
            return path
        return path + ('index.html' if self.index_file else '')

    @property
    def parent_url(self):
        return self.url.rstrip('/').rsplit('/', 1)[0] + '/'

    @property
    def parent(self):
        return self.pages[self.parent_url]

    @property
    def children(self):
        children = []
        for page in self.pages.values():
            if page.archive or page.parent_url != self.url:
                continue
            page = fix_urls(Page(page.get()))
            children += [(page.url, page)]
        children.sort(key=lambda v: v[1].sort, reverse=True)
        return OrderedDict(children)

    @property
    def terms(self):
        if not self.body:
            return

        terms = self.pages.get(self.terms_file)
        if not terms:
            print(' * WARN. No terms file "%s"' % self.terms_file)
            return

        root = parse_xml(self.body, self.index_file)
        links = root.xpath('//a[starts-with(@href, "#term-")]')
        if not links:
            return

        result = []
        terms_ = parse_xml(terms.body, terms.src('index_file'))
        for link in links:
            id = link.get('href')[1:]
            term = terms_.xpath('//*[@id=\'%s\']' % id)
            if not term:
                print(' * WARN. No term "%s" for "%s"' % (id, self.index_file))
                continue
            result += term[:1]

        result = [etree.tostring(t, encoding='utf8').decode() for t in result]
        Terms = namedtuple('Terms', 'title body')
        return Terms(terms.title, '\n'.join(result))


def get_pages(src_dir, use_cache=False, check_xml=False):
    get = lambda **d: get_page(d, use_cache)

    tree = OrderedDict((f[0], (f[1], f[2])) for f in os.walk(src_dir))
    paths = reversed(list(tree.keys()))

    pages = OrderedDict()
    ### Create pages by directories
    for path in paths:
        url = path.replace(src_dir, '') + '/'
        if not os.path.isdir(path) or url.rsplit('/', 2)[1].startswith('_'):
            continue

        files = tree[path][1]
        meta = META_FILE if META_FILE in files else None
        index = ([f for f in INDEX_FILES if f in files] or [None])[0]

        pages[url] = get(
            pages=pages,
            url=url,
            src_dir=src_dir,
            index_file=index and url + index,
            meta_file=meta and url + meta
        )

    ### Create pages for global "url-files"
    for index_file in get_globals(src_dir, 'url-files', []):
        path = src_dir + index_file
        if not os.path.exists(path):
            print(' * WARN. File not exists - {}'.format(path))
            continue
        url = index_file.rsplit('.', 1)[0]
        pages[url] = get(
            pages=pages,
            url=url,
            src_dir=src_dir,
            index_file=index_file,
            archive=True
        )

    ### Save HTML to index_file
    env = get_jinja(src_dir)
    for page in pages.values():
        if page.url == '/naspeh/':
            page.terms
        if not page.index_file:
            continue

        if page.template:
            tpl = env.get_template(page.template)
            page.update(text=tpl.render(p=page))

        if page.type == 'inc':
            text = do_includes(page.index_file, src_dir)
            page.update(text=text)

        with open(page.path, 'bw') as f:
            f.write(page.text.encode())

        if check_xml and page.path.rsplit('.', 1)[1] in ('html', 'xml'):
            parse_xml(page.text, page.template or page.index_file, quiet=True)

    return pages


def get_summary(data):
    summary = re.search('(?s)^(.*?)<!--\s*MORE\s*-->', data)
    if summary:
        summary = summary.group(1)
    return summary or None


def get_globals(src_dir, key=None, default=None):
    if not hasattr(get_globals, 'cache'):
        meta = {}
        meta_file = os.path.join(src_dir, META_FILE)
        if os.path.exists(meta_file):
            with open(meta_file, 'br') as f:
                meta = json.loads(f.read().decode())
            meta = meta.get('globals') or {}
            if 'timezone' in meta:
                tz = timezone(meta['timezone'])
            else:
                tz = utc
            meta['tz'] = tz
            meta['now'] = utc.localize(dt.datetime.utcnow()).astimezone(tz)

        get_globals.cache = meta
    if key is not None:
        return get_globals.cache.get(key, default)
    return get_globals.cache


def do_includes(filename, src_dir):
    '''Process includes for css and javascript files'''
    def load(match):
        filename = match.groups(1)[0]
        filename = os.path.join(src_dir, filename)
        if not os.path.exists(filename):
            print(' * ERROR. no file: "%s"' % filename)
            return match.group()

        with open(filename, 'br') as f:
            text = f.read().decode()
        return text

    with open(src_dir + filename, 'br') as f:
        text = f.read().decode()
    text = re.sub(r'\/\* @include ([^ ]*) \*\/', load, text)
    return text


def get_jinja(src_dir):
    env = Environment(
        loader=FileSystemLoader(src_dir),
        lstrip_blocks=True, trim_blocks=True
    )
    env.filters.update({
        'rst': lambda text: rst(text)[1],
        'markdown': markdown,
        'match': lambda value, pattern: re.match(pattern, value)
    })
    env.globals.update(get_globals(src_dir))
    return env


def get_page(data, use_cache=False):
    page = Page(data)
    if not use_cache:
        return fill_page(page)

    cache_file = page.path + CACHE_FILE
    if os.path.exists(cache_file):
        with open(cache_file, 'br') as f:
            data = pickle.loads(f.read())
            page.update(**dict(data, pages=page.pages))
    else:
        page = fill_page(page)
        with open(cache_file, 'bw') as f:
            f.write(pickle.dumps(dict(page.get(), pages=None)))
    return page


def fill_page(page):
    if page.meta_file:
        page.update(**page.get_meta())

    if page.index_file:
        with open(page.src('index_file'), 'br') as f:
            text = f.read().decode()

        if page.type == 'py':
            subprocess.call(
                'cd {} && python index.py'
                .format(page.src_dir + page.url),
                shell=True
            )
            with open(page.path, 'br') as f:
                text = f.read().decode()
            page.update(text=text)

        elif page.type == 'html':
            page.update(text=text)

        elif page.type == 'tpl':
            page.update(template=page.index_file)

        elif page.type == 'md':
            body = markdown(text)
            page.update(body=body, summary=get_summary(body))

        elif page.type == 'rst':
            title, body = rst(text, source_path=page.src('index_file'))
            if title:
                page.update(title=title)
            page.update(body=body, summary=get_summary(body))

        # Need template render
        if page.type in ['rst', 'md']:
            page.update(template=page.get('template') or '_theme/base.tpl')

    return page


def parse_xml(text, base_file, quiet=False):
    try:
        data = re.sub('(?i)<(!DOCTYPE|\?xml).*?[^>]>', '', text)
        root = etree.fromstring('<root>%s</root>' % data)
    except etree.ParseError as e:
        if quiet:
            print(' * WARN. {}: "{}"'.format(base_file, e))
            root = None
        else:
            raise
    return root


def fix_urls(page):
    host = get_globals(page.src_dir, 'host')

    def fix_url(element, attr):
        url = element.attrib.get(attr)
        if not url.startswith('http://'):
            element.attrib[attr] = urljoin(host + page.url, url)

    def fix_urls(text):
        root = parse_xml(text, page.index_file)
        for img in root.findall('.//img'):
            fix_url(img, 'src')
        for link in root.findall('.//a'):
            fix_url(link, 'href')
        text = etree.tostring(root, encoding="UTF-8").decode()
        text = text[6: -7]
        return text

    for part in ['title', 'summary', 'body']:
        text = getattr(page, part)
        if text:
            page.update(**{part: fix_urls(text)})
    return page


def markdown(text):
    from markdown2 import Markdown

    md = Markdown(extras=['footnotes', 'code-friendly', 'code-color'])
    return md.convert(text)


def rst(source, source_path=None):
    from docutils.core import publish_parts

    parts = publish_parts(
        source=source,
        source_path=source_path,
        writer_name='html',
        settings_overrides={
            'syntax_highlight': 'short',
            'trim_footnote_reference_space': True,
            'smart_quotes': True,
            'cloak_email_addresses': True,
            'traceback': True
        }
    )
    return parts['title'], parts['body']


def clean_dir(dest_dir, skip_dir=False):
    for path in os.listdir(dest_dir):
        path = os.path.join(dest_dir, path)
        if os.path.isdir(path):
            if not skip_dir:
                shutil.rmtree(path)
        else:
            os.unlink(path)


def copy_dir(src_dir, dest_dir):
    for path in os.listdir(src_dir):
        src_path = os.path.join(src_dir, path)
        dest_path = os.path.join(dest_dir, path)
        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                shutil.copytree(src_path, dest_path)
        else:
            shutil.copy2(src_path, dest_path)


def build(src_dir, build_dir, nginx_file=None, use_cache=False):
    '''Build static site from `src_dir`'''
    start = time.time()

    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    if use_cache:
        all_files = list_files(src_dir)
        cache_file = os.path.join(build_dir, CACHE_FILE)
        if os.path.exists(cache_file):
            with open(cache_file, 'br') as f:
                last_files = pickle.loads(f.read())
            del_, new_, mod_, changes = diff_files(all_files, last_files)
            if changes:
                _dir = lambda f: f.replace(src_dir, '').rsplit('/', 1)[0] + '/'
                for file in set(del_ + mod_):
                    path = build_dir + _dir(file)
                    clean_dir(path, skip_dir=True)

                for file in set(new_ + mod_ + del_):
                    paths = [d + _dir(file) for d in [src_dir, build_dir]]
                    copy_dir(*paths)
            else:
                print(' * No changes')

        with open(cache_file, 'bw') as f:
            f.write(pickle.dumps(all_files))
    else:
        clean_dir(build_dir)
        copy_dir(src_dir, build_dir)

    pages = get_pages(build_dir, use_cache, check_xml=True)
    save_rules(pages, nginx_file or os.path.join(build_dir, '.nginx'))
    save_urls(pages, os.path.join(src_dir, URLS_FILE))
    print(' * Build successful (during %.3fs)' % (time.time() - start))


def save_rules(pages, nginx_file):
    '''Save rewrite rules for nginx'''
    urls = []
    for url, page in pages.items():
        if page.text:
            urls += [(url, page, False)]
            aliases = page.aliases or []
            aliases += [
                a.rstrip('/') for a in aliases
                if a.rstrip('/') and a.rstrip('/') != a
            ]
            aliases = set(aliases)
            urls += [(a, page, True) for a in aliases]

    rules = set(
        (u.rstrip('/'), p.url) for u, p, is_alias in urls
        if is_alias and u.rstrip('/') != p.url.rstrip('/')
    )
    if rules:
        rules = ['rewrite ^{}/?$ {} permanent;'.format(u, p) for u, p in rules]
        rules = '\n'.join(rules)
        with open(nginx_file, 'bw') as f:
            f.write(rules.encode())


def save_urls(pages, filename):
    urlmap = dict(
        [url, page.aliases]
        for url, page in pages.items()
        if page.text
    )
    urlmap = json.dumps(
        urlmap, sort_keys=True, indent=4, separators=(',', ': ')
    )

    urlmap_prev = None
    if os.path.exists(filename):
        with open(filename, 'br') as f:
            urlmap_prev = f.read().decode()

    if not urlmap_prev or urlmap_prev != urlmap:
        with open(filename, 'bw') as f:
            f.write(urlmap.encode())


def run(src_dir, build_dir, port=5000, no_build=False, no_cache=False):
    if not no_build:
        build(src_dir, build_dir, use_cache=not no_cache)

    watcher = Thread(target=watch_files, args=(src_dir, 1, not no_cache))
    watcher.daemon = True
    watcher.start()

    os.chdir(build_dir)
    http.server.test(http.server.SimpleHTTPRequestHandler, port=port)


def list_files(path):
    ignore = [os.path.join(path, f) for f in [URLS_FILE, CACHE_FILE]]

    files = list()
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if filepath in ignore:
                continue

            try:
                mtime = os.stat(filepath).st_mtime
            except OSError:
                continue
            files.append([filepath, mtime])
    return OrderedDict(sorted(files, key=lambda v: v[0]))


def diff_files(files, old_files, quiet=False):
    del_, new_, mod_ = [], [], []

    files_ = set(files.keys())
    old_files_ = set(old_files.keys())
    if files_ != old_files_:
        del_ = list(old_files_ - files_)
        new_ = list(files_ - old_files_)

    for filename, mtime in files.items():
        if mtime > old_files.get(filename, mtime):
            mod_ += [filename]

    changes = []
    changes += ['deleted file(s) %s' % ', '.join(del_)] if del_ else []
    changes += ['new file(s) %s' % ', '.join(new_)] if new_ else []
    changes += ['modified file(s) %s' % ', '.join(mod_)] if mod_ else []
    if not quiet and changes:
        print('\n -- '.join([' * Detected changes, rebuild'] + changes))
    return del_, new_, mod_, changes


def watch_files(src_dir, interval=1, use_cache=True):
    old_files = None
    while 1:
        files = list_files(src_dir)
        old_files = files if old_files is None else old_files

        changes = diff_files(files, old_files, use_cache)[-1]
        if changes:
            cmd = '%s build%s' % (__file__, ' -c' if use_cache else '')
            subprocess.call(cmd, shell=True, cwd=ROOT_DIR)

        old_files = files
        time.sleep(interval)


def check_urls(host=None, verbose=False):
    log = lambda *a: verbose and print(*a)

    if not host:
        if not os.path.exists(BUILD_DIR):
            process('build')
        host = 'localhost:9000'
        args = 'run --port=9000 --no-build'.split(' ')
        server = Thread(target=process, args=args)
        server.daemon = True
        server.start()
        time.sleep(1)

    with open(os.path.join(SRC_DIR, URLS_FILE), 'br') as f:
        urls = json.loads(f.read().decode())

    def get(url, expected_code=200, indent=''):
        comment = ''
        try:
            conn = http.client.HTTPConnection(host)
            conn.request('HEAD', url)
            res = conn.getresponse()
            code = res.status
            if code == 200:
                res_url = url
            else:
                res_url = res.info().get('Location', '')
                res_url = res_url.replace('http://' + host, '')
        except HTTPError as e:
            code = e.code
            res_url = None

        err = []
        if code != expected_code:
            err = ['%s (%r != %r)' % (url, code, expected_code)]
        else:
            log('%s%s %s %s # %s' % (indent, url, code, res_url, comment))
        return err

    all_aliases = []
    for aliases in urls.values():
        all_aliases += aliases or []

    err = []
    for url in sorted(urls.keys()):
        aliases = urls.get(url)
        err += get(url, expected_code=301 if url in all_aliases else 200)
        for alias in aliases or []:
            err += get(alias, expected_code=301, indent='  ')
    if err:
        print('Errors:')
        print('\n'.join(err))
    else:
        print('OK')


def get_parser():
    parser = argparse.ArgumentParser()
    cmds = parser.add_subparsers(title='commands')

    def cmd(name, **kw):
        p = cmds.add_parser(name, **kw)
        p.set_defaults(cmd=name)
        p.arg = lambda *a, **kw: p.add_argument(*a, **kw) and p
        p.exe = lambda f: p.set_defaults(exe=f) and p
        return p

    cmd('run', help='start dev server')\
        .arg('-p', '--port', type=int, default=5000)\
        .arg('--no-build', action='store_true')\
        .arg('--no-cache', action='store_true')\
        .exe(lambda a: run(SRC_DIR, BUILD_DIR, a.port, a.no_build, a.no_cache))

    cmd('build', help='build static content from `data` directory')\
        .arg('-b', '--bdir', default=BUILD_DIR, help='build directory')\
        .arg('-n', '--nginx-file', help='file nginx rules')\
        .arg('-p', '--port', type=int, default=8000)\
        .arg('-c', '--use-cache', action='store_true')\
        .exe(lambda a: build(SRC_DIR, a.bdir, a.nginx_file, a.use_cache))

    cmd('test_urls', help='test url responses')\
        .arg('-v', '--verbose', action='store_true')\
        .arg('-H', '--host', help='use host for test')\
        .exe(lambda a: check_urls(host=a.host, verbose=a.verbose))

    return parser, cmd


def process(*args, parser=None):
    if parser is None:
        parser, _ = get_parser()

    args = parser.parse_args(args or None)
    if not hasattr(args, 'cmd'):
        parser.print_usage()
    elif hasattr(args, 'exe'):
        args.exe(args)
    else:
        raise ValueError('Wrong subcommand')


if __name__ == '__main__':
    process()
