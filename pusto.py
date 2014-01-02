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
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader
from pytz import timezone, utc


ROOT_DIR = os.getcwd()
SRC_DIR = ROOT_DIR + '/data'
BUILD_DIR = ROOT_DIR + '/build'
CACHE_FILE = '.last'
URLS_FILE = 'urls.json'
META_FILES = ['meta.json']
INDEX_FILES = ['index.' + t for t in 'py html tpl rst md'.split(' ')]


class Page(namedtuple('Page', (
    'pages url path type index_file meta_file mtime '
    'template params aliases published sort author archive '
    'title summary body html'
))):
    __slots__ = ()

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
            children += [(page.url, fix_urls(page, get_globals('host')))]
        children.sort(key=lambda v: v[1].sort, reverse=True)
        return OrderedDict(children)


def get_urls(src_dir):
    pages = get_cached_pages(src_dir)

    urls = []
    for url, page in pages.items():
        if page.html:
            urls += [(url, page, False)]
            aliases = page.aliases or []
            aliases += [
                a.rstrip('/') for a in (aliases + [url])
                if a.rstrip('/') and a.rstrip('/') != a
            ]
            aliases = set(aliases)
            urls += [(a, page, True) for a in aliases]
    return urls, pages


def get_cached_pages(src_dir):
    cachefile = os.path.join(src_dir, CACHE_FILE)
    all_files = list_files(src_dir)

    cache = {}
    if os.path.exists(cachefile):
        with open(cachefile, 'br') as cf:
            cache, last_files = pickle.loads(cf.read())
        changes = sum(diff_files(all_files, last_files), [])

        for url in list(cache.keys()):
            for change in changes:
                patern = change.replace(src_dir, '').rsplit('/', 1)[0] + '/'
                url_ = url.rsplit('/', 1)[0]  # remove file in tail if exists
                if patern.startswith(url_) or url_.startswith(patern):
                    del cache[url]

    pages = get_pages(src_dir, cache)

    with open(cachefile, 'bw') as f:
        cache = dict(
            (k, v._replace(pages=None)._asdict())
            for k, v in pages.items()
        )
        f.write(pickle.dumps([cache, all_files]))

    return pages


def get_pages(src_dir, cache=None):
    cache = cache or {}

    tree = OrderedDict((f[0], (f[1], f[2])) for f in os.walk(src_dir))
    paths = reversed(list(tree.keys()))

    pages = OrderedDict()
    ### Create pages by directories
    for path in paths:
        url = path.replace(src_dir, '') + '/'
        if not os.path.isdir(path) or url.rsplit('/', 2)[1].startswith('_'):
            continue

        files = tree[path][1]
        meta = ([f for f in META_FILES if f in files] or [None])[0]
        index = ([f for f in INDEX_FILES if f in files] or [None])[0]

        page = get_html(src_dir, cache=cache, ctx={
            'pages': pages, 'url': url,
            'index_file': index and url + index,
            'meta_file': meta and url + meta,
            'type': index and index.rsplit('.', 1)[1],
            'path': (src_dir + url + 'index.html') if index else src_dir
        })
        pages[url] = page

    ### Create pages for "url-files"
    for index_file in get_globals('url-files', []):
        path = src_dir + index_file
        if not os.path.exists(path):
            print(' * WARN. File not exists - {}'.format(path))
            continue
        path, type_ = path.rsplit('.', 1)
        url = path.replace(src_dir, '')
        page = get_html(src_dir, cache=cache, ctx={
            'pages': pages, 'url': url,
            'index_file': index_file,
            'meta_file': None,
            'type': type_,
            'path': path,
        })
        pages[url] = page._replace(archive=True)

    ### Generate HTML for pages via jinja2 if template exists
    env = get_jinja(src_dir)
    for page in pages.values():
        if page.template:
            tpl = env.get_template(page.template)
            html = tpl.render(p=page)
            with open(page.path, 'bw') as f:
                f.write(html.encode())
            pages[page.url] = page._replace(html=html)
    return pages


def bind_meta(ctx, data, method=None):
    meta = data
    if method == 'html':
        meta = re.search('(?s)<!--\s*META(\s*\{.*})\s*-->', data)
        if meta:
            meta = meta.group(1)
            meta = json.loads(meta)
        else:
            meta = {}

        summary = re.search('(?s)^(.*?)<!--\s*MORE\s*-->', data)
        if summary:
            summary = summary.group(1)
            summary = re.sub('(?s)<!--.*?-->', '', summary)
            meta['summary'] = summary

    elif method == 'json':
        meta = json.loads(meta)

    published = ''
    if 'published' in meta:
        published = dt.datetime.strptime(meta['published'], '%d.%m.%Y')
        published = published.replace(hour=8)
        published = get_globals('tz').localize(published)
        meta['published'] = published

    keys = (
        'published sort author aliases archive template params '
        'summary title body'
        .split(' ')
    )
    for key in keys:
        ctx.setdefault(key, None)
        if key in meta:
            ctx[key] = meta[key]

    if not ctx['sort'] and 'sort' not in meta:
        ctx['sort'] = published and published.isoformat()


def get_globals(key=None, default=None):
    if not hasattr(get_globals, 'cache'):
        meta = {}
        meta_file = os.path.join(SRC_DIR, META_FILES[0])
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


def get_jinja(src_dir):
    if not hasattr(get_jinja, 'cache'):
        env = Environment(
            loader=FileSystemLoader(src_dir),
            lstrip_blocks=True, trim_blocks=True
        )
        env.filters.update({
            'rst': lambda text: rst(text)[1],
            'markdown': markdown,
            'match': lambda value, pattern: re.match(pattern, value)
        })
        env.globals.update(get_globals())
        get_jinja.cache = env
    return get_jinja.cache


def get_html(src_dir, ctx, cache=None):
    meta_file = ctx['meta_file']
    if meta_file:
        with open(src_dir + meta_file, 'br') as f:
            meta = f.read().decode()
        bind_meta(ctx, meta, method='json')
    else:
        bind_meta(ctx, {})

    index_file = ctx['index_file']
    if not index_file:
        html = None
        mtime = None
    else:
        cpage = cache.get(ctx['url'])
        if cpage:
            return Page(**dict(cpage, pages=ctx['pages']))

        html = None
        template = ctx.get('template') or '_theme/base.tpl'
        index_src = src_dir + index_file
        mtime = dt.datetime.fromtimestamp(os.stat(index_src).st_mtime)
        with open(index_src, 'br') as f:
            text = f.read().decode()

        if ctx['type'] == 'py':
            subprocess.call(
                'cd {} && python index.py'
                .format(src_dir + ctx['url']),
                shell=True
            )
            with open(ctx['path'], 'br') as f:
                html = f.read().decode()
            bind_meta(ctx, html, method='html')

        elif ctx['type'] == 'html':
            html = text
            bind_meta(ctx, html, method='html')

        elif ctx['type'] == 'tpl':
            ctx.update(template=index_file)

        elif ctx['type'] == 'md':
            body = markdown(text)
            bind_meta(ctx, body, method='html')
            ctx.update(body=body, template=ctx.get('template') or template)

        elif ctx['type'] == 'rst':
            title, body = rst(text, source_path=index_src)
            bind_meta(ctx, body, method='html')
            if title:
                ctx['title'] = title
            ctx.update(body=body, template=ctx.get('template') or template)

    ctx.update(html=html, mtime=mtime)
    return Page(**ctx)


def parse_xml(text, base_file, quiet=False):
    try:
        data = re.sub('(?i)<(!DOCTYPE|\?xml).*?[^>]>', '', text)
        root = ET.fromstring('<root>%s</root>' % data)
    except ET.ParseError as e:
        if quiet:
            print(' * WARN. {}: "{}"'.format(base_file, e))
            root = None
        else:
            raise
    return root


def fix_urls(page, host):
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
        text = ET.tostring(root, encoding="UTF-8").decode()
        text = text[6: -7]
        return text

    for part in ['title', 'summary', 'body']:
        text = getattr(page, part)
        if text:
            page = page._replace(**{part: fix_urls(text)})
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


def build(src_dir, build_dir, nginx_file=None, with_cache=False):
    '''Build static site from `src_dir`'''
    start = time.time()
    if os.path.exists(build_dir):
        cachefile = os.path.join(build_dir, CACHE_FILE)
        for path in os.listdir(build_dir):
            path = os.path.join(build_dir, path)
            if with_cache and path == cachefile:
                continue
            elif os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)
        for path in os.listdir(src_dir):
            src_path = os.path.join(src_dir, path)
            build_path = os.path.join(build_dir, path)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, build_path)
            else:
                shutil.copy2(src_path, build_path)
    else:
        shutil.copytree(src_dir, build_dir)

    urls, pages = get_urls(build_dir)
    save_rules(urls, nginx_file or os.path.join(build_dir, '.nginx'))
    save_urls(pages, os.path.join(src_dir, URLS_FILE))
    check_xml(pages)
    print(' * Build successful (during %.3fs)' % (time.time() - start))
    return urls


def check_xml(pages):
    for page in pages.values():
        if page.html:
            parse_xml(page.html, page.index_file, quiet=True)


def save_rules(urls, nginx_file):
    '''Save rewrite rules for nginx'''
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
        if page.index_file
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


def run(src_dir, build_dir, no_build=False, port=5000):
    if not no_build:
        build(src_dir, build_dir)

    watcher = Thread(target=watch_files, args=(src_dir,))
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


def diff_files(files, old_files):
    del_, new_, mod_ = [], [], []

    files_ = set(files.keys())
    old_files_ = set(old_files.keys())
    if files_ != old_files_:
        del_ = list(old_files_ - files_)
        new_ = list(files_ - old_files_)

    for filename, mtime in files.items():
        if mtime > old_files.get(filename, mtime):
            mod_ += [filename]
    return del_, new_, mod_


def watch_files(src_dir, interval=1):
    old_files = None
    while 1:
        files = list_files(src_dir)
        old_files = files if old_files is None else old_files

        del_, new_, mod_ = diff_files(files, old_files)
        changes = []
        changes += ['deleted file(s) %s' % ', '.join(del_)] if del_ else []
        changes += ['new file(s) %s' % ', '.join(new_)] if new_ else []
        changes += ['modified file(s) %s' % ', '.join(mod_)] if mod_ else []

        if changes:
            changes = [' * Detected changes, rebuild'] + changes
            print('\n    '.join(changes))
            subprocess.call('%s build -c' % __file__, shell=True, cwd=ROOT_DIR)

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
        .arg('--no-build', action='store_true')\
        .arg('--port', type=int, default=5000)\
        .exe(lambda a: run(SRC_DIR, BUILD_DIR, a.no_build, a.port))

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
