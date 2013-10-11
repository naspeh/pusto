#!/usr/bin/env python
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import time
from collections import namedtuple, OrderedDict
from http.client import HTTPConnection
from threading import Thread
from urllib.error import HTTPError
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader, Template
from werkzeug.exceptions import NotFound
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

Page = namedtuple('Page', (
    'url children index_file meta_file type path '
    'aliases published author hidden template sort title summary body html'
))

ROOT_DIR = os.getcwd()
SRC_DIR = ROOT_DIR + '/data'
BUILD_DIR = ROOT_DIR + '/build'
META_FILES = ['meta.json']
INDEX_FILES = ['index.' + t for t in 'py html tpl rst md'.split(' ')]


def get_urls(src_dir):
    pages = get_pages(src_dir)

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


def get_pages(src_dir):
    tree = OrderedDict((f[0], (f[1], f[2])) for f in os.walk(src_dir))
    paths = list(tree.keys())
    paths.reverse()

    pages = OrderedDict()
    for path in paths:
        url = path.replace(src_dir, '') + '/'
        if not os.path.isdir(path) or url.rsplit('/', 2)[1].startswith('_'):
            continue

        files = tree[path][1]
        meta = ([f for f in META_FILES if f in files] or [None])[0]
        index = ([f for f in INDEX_FILES if f in files] or [None])[0]
        children = [
            (k, v) for k, v in pages.items()
            if k.rsplit('/', 2)[0] + '/' == url and not v.hidden
        ]
        children.sort(key=lambda v: v[1].sort, reverse=True)
        children = OrderedDict(children)
        ctx = get_html(src_dir, dict(
            url=url, children=children,
            index_file=index and url + index,
            meta_file=meta and url + meta,
            type=index and index.rsplit('.', 1)[1]
        ))
        pages[url] = ctx

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

        try:
            data = re.sub('(?i)<(!DOCTYPE|\?xml).*?[^>]>', '', data)
            root = ET.fromstring('<root>%s</root>' % data)
            summary = root.findall('*[@id="summary"]')
            if summary:
                summary = ET.tostring(summary[0], 'utf8', 'html')
                meta['summary'] = summary.decode()
        except ET.ParseError as e:
            print('WARN: {}: "{}"'.format(ctx['index_file'], e))

    elif method == 'json':
        meta = json.loads(meta)

    if 'author' in meta:
        author = meta['author']
        author = (
            (author.count('naspeh') and ['Гриша'] or []) +
            (author.count('nayavu') and ['Катя'] or [])
        )
        author = (
            ('Автор: ' if len(author) == 1 else 'Авторы: ') +
            ' и '.join(author)
        )
        meta['author'] = author

    published = ''
    if 'published' in meta:
        published = dt.datetime.strptime(meta['published'], '%d.%m.%Y')
        meta['published'] = published

    keys = (
        'published author aliases hidden template sort summary title body'
        .split(' ')
    )
    for key in keys:
        ctx.setdefault(key, None)
        if key in meta:
            ctx[key] = meta[key]

    if 'sort' not in meta and not ctx['sort']:
        ctx['sort'] = published and published.isoformat()


def get_jinja(src_dir):
    if not hasattr(get_jinja, 'env'):
        env = Environment(
            loader=FileSystemLoader(src_dir),
            lstrip_blocks=True, trim_blocks=True
        )
        env.filters.update({
            'rst': lambda text: rst(text)[1],
            'markdown': markdown
        })
        get_jinja.env = env
    return get_jinja.env


def get_html(src_dir, ctx):
    env = get_jinja(src_dir)

    meta_file = ctx['meta_file']
    if meta_file:
        with open(src_dir + meta_file, 'br') as f:
            meta = f.read().decode()
        bind_meta(ctx, meta, method='json')
    else:
        bind_meta(ctx, {})

    index_file = ctx['index_file']
    if not index_file:
        path = src_dir
        html = None
    else:
        path = src_dir + ctx['url'] + 'index.html'
        index_src = src_dir + index_file
        with open(index_src, 'br') as f:
            text = f.read().decode()

        if ctx['type'] == 'py':
            subprocess.call(
                'cd {} && python index.py'
                .format(src_dir + ctx['url']),
                shell=True
            )
            with open(path, 'br') as f:
                html = f.read().decode()
            bind_meta(ctx, html, method='html')

        elif ctx['type'] == 'html':
            html = text
            bind_meta(ctx, html, method='html')

        elif ctx['type'] == 'tpl':
            tpl = env.get_template(index_file)
            html = tpl.render(ctx, page=ctx)
            bind_meta(ctx, html, method='html')

        elif ctx['type'] == 'md':
            body = markdown(text)
            bind_meta(ctx, body, method='html')
            ctx.update(body=body)
            tpl = env.get_template('/_theme/base.tpl')
            html = tpl.render(ctx, page=ctx)

        elif ctx['type'] == 'rst':
            title, body = rst(text, source_path=index_src)
            bind_meta(ctx, body, method='html')
            if title:
                ctx['title'] = title
            ctx['body'] = body

            tpl = ctx.get('template', None) or '/_theme/base.tpl'
            tpl = env.get_template(tpl)
            html = tpl.render(ctx, page=ctx)

    ctx.update(html=html, path=path)
    return Page(**ctx)


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


def build(src_dir, build_dir, nginx_file=None):
    '''Build static site from `src_dir`'''
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    config = {'noindex': None, 'host': 'http://example.com'}
    config_file = os.path.join(build_dir, 'config.json')
    if os.path.exists(config_file):
        with open(config_file, 'br') as f:
            config.update(json.loads(f.read().decode()))

    urls, pages = get_urls(build_dir)
    for url, page, is_alias in urls:
        if is_alias:
            continue
        elif url == page.index_file and not page.index_file.endswith('.html'):
            with open(page.path, 'bw') as f:
                f.write(page.html.encode())

    save_rules(urls, nginx_file or os.path.join(build_dir, '.nginx'))
    save_urls(pages, os.path.join(src_dir, 'urls.json'))
    save_sitemap(pages, os.path.join(build_dir, 'sitemap.xml'), config)
    print(' * Build successful')
    return urls


def save_rules(urls, nginx_file):
    '''Save rewrite rules for nginx'''
    rules = set((u.rstrip('/'), u) for u, _, is_alias in urls if is_alias)
    if rules:
        rules = ['rewrite ^{}/?$ {} permanent;'.format(u, p) for u, p in rules]
        rules = '\n'.join(rules)
        with open(nginx_file, 'bw') as f:
            f.write(rules.encode())


def save_sitemap(pages, filename, config):
    if config['noindex']:
        pages = [
            p for p in pages.values()
            if not re.match(config['noindex'], p.url)
        ]
    tpl = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        '    {% for page in pages %}'
        '    <url>'
        '        <loc>{{ host }}{{ page.url }}</loc>'
        '    </url>'
        '    {% endfor %}'
        '</urlset>'
    )
    tpl = Template(tpl)
    sitemap = tpl.render(pages=pages, host=config['host'])
    with open(filename, 'bw') as f:
        f.write(sitemap.encode())


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


def list_files(path):
    files = set()
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            if filename not in files:
                files.add(filename)
    return sorted(files)


def watch_files(src_dir, build_dir, interval=1):
    ignore = [os.path.join(src_dir, 'urls.json')]
    mtimes = {}
    old_files = None
    while 1:
        changes = []
        files = list_files(src_dir)
        old_files = files if old_files is None else old_files
        if files != old_files:
            del_files = set(old_files) - set(files)
            new_files = set(files) - set(old_files)
            if del_files or new_files:
                if del_files:
                    changes += ['deleted file(s) %s' % ', '.join(del_files)]
                if new_files:
                    changes += ['new file(s) %s' % ', '.join(new_files)]

        mod_files = []
        for filename in files:
            filename_ = os.path.join(src_dir, filename)
            if filename_ in ignore:
                continue
            try:
                mtime = os.stat(filename_).st_mtime
            except OSError:
                continue

            old_time = mtimes.get(filename)
            mtimes[filename] = mtime
            if old_time and mtime > old_time:
                mod_files += [filename]
        if mod_files:
            changes += ['modified file(s) %s' % ', '.join(mod_files)]

        if changes:
            changes = [' * Detected changes, rebuild'] + changes
            print('\n    '.join(changes))
            build(src_dir, build_dir)

        old_files = files
        time.sleep(interval)


def create_app(build_dir, debug=False):
    '''Create WSGI application'''
    def _urls():
        if not hasattr(_urls, 'cache'):
            pages, _ = get_urls(build_dir)
            urls = []
            for url, page, is_alias in pages:
                if is_alias:
                    urls += [(url, redirect(page.url, 301))]
                else:
                    urls += [(url, Response(page.html, mimetype='text/html'))]
            _urls.cache = dict(urls)
        return _urls.cache

    @Request.application
    def app(request):
        response = _urls().get(request.path, None)
        if response:
            return response

        return NotFound()
    return app


def check_urls(host=None, verbose=False):
    log = lambda *a: verbose and print(*a)

    if not host:
        if not os.path.exists(BUILD_DIR):
            process('build')
        host = 'localhost:9000'
        args = 'run --port=9000 --no-reloader --no-build'.split(' ')
        server = Thread(target=process, args=args)
        server.daemon = True
        server.start()
        time.sleep(1)

    with open('data/urls.json', 'br') as f:
        urls = json.loads(f.read().decode())

    def get(url, expected_code=200, indent=''):
        comment = ''
        try:
            conn = HTTPConnection(host)
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

    err = []
    for url in sorted(urls.keys()):
        aliases = urls.get(url)
        err += get(url)
        for alias in aliases or []:
            err += get(alias, expected_code=301, indent='  ')
    if err:
        print('Errors:')
        print('\n'.join(err))
    else:
        print('OK')


def process(*args):
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(title='subcommands')

    def sub(name, **kw):
        s = subs.add_parser(name, **kw)
        s.set_defaults(sub=name)
        s.arg = lambda *a, **kw: s.add_argument(*a, **kw) and s
        return s

    sub('run', help='start dev server')\
        .arg('--host', default='localhost')\
        .arg('--port', type=int, default=5000)\
        .arg('--no-reloader', action='store_true')\
        .arg('--no-build', action='store_true')

    sub('build', help='build static content from `data` directory')\
        .arg('-b', '--bdir', default=BUILD_DIR, help='build directory')\
        .arg('-n', '--nginx-file', help='file nginx rules')\
        .arg('--port', type=int, default=8000)

    sub('test_urls', help='test url responses')\
        .arg('-v', '--verbose', action='store_true')\
        .arg('--host', help='use host for test')\

    args = parser.parse_args(args or None)
    if not hasattr(args, 'sub'):
        parser.print_usage()

    elif args.sub == 'run':
        run_main = os.environ.get('WERKZEUG_RUN_MAIN')
        if not args.no_build and not run_main:
            build(SRC_DIR, BUILD_DIR)

        if not args.no_reloader and run_main:
            watcher = Thread(target=watch_files, args=(SRC_DIR, BUILD_DIR))
            watcher.daemon = True
            watcher.start()

        run_simple(
            args.host, args.port, create_app(BUILD_DIR, debug=True),
            use_reloader=not args.no_reloader, use_debugger=True,
            static_files={'': BUILD_DIR},
            extra_files=[os.path.join(BUILD_DIR, '.nginx')]
        )

    elif args.sub == 'build':
        build(SRC_DIR, args.bdir, args.nginx_file)

    elif args.sub == 'test_urls':
        check_urls(host=args.host, verbose=args.verbose)
    else:
        raise ValueError('Wrong subcommand')


if __name__ == '__main__':
    process()
