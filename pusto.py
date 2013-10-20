#!/usr/bin/env python
import argparse
import datetime as dt
import http.client
import http.server
import json
import os
import re
import shutil
import subprocess
import time
from collections import namedtuple, OrderedDict
from threading import Thread
from urllib.error import HTTPError
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader

Page = namedtuple('Page', (
    'url children index_file meta_file type path '
    'aliases published author archive template sort '
    'title summary body html'
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
            if k.rsplit('/', 2)[0] + '/' == url and not v.archive
        ]
        children.sort(key=lambda v: v[1].sort, reverse=True)
        children = OrderedDict(children)
        ctx = get_html(src_dir, {
            'url': url, 'children': children,
            'index_file': index and url + index,
            'meta_file': meta and url + meta,
            'type': index and index.rsplit('.', 1)[1]
        })
        pages[url] = ctx

    env = get_jinja(src_dir)
    for page in pages.values():
        if page.template:
            tpl = env.get_template(page.template)
            html = tpl.render(page._asdict(), page=page, pages=pages)
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
        meta['published'] = published

    keys = (
        'published author aliases archive template sort summary title body'
        .split(' ')
    )
    for key in keys:
        ctx.setdefault(key, None)
        if key in meta:
            ctx[key] = meta[key]

    if not ctx['sort'] and 'sort' not in meta:
        ctx['sort'] = published and published.isoformat()


def get_jinja(src_dir):
    if not hasattr(get_jinja, 'env'):
        env = Environment(
            loader=FileSystemLoader(src_dir),
            lstrip_blocks=True, trim_blocks=True
        )
        env.filters.update({
            'rst': lambda text: rst(text)[1],
            'markdown': markdown,
            'match': lambda value, pattern: re.match(pattern, value)
        })
        get_jinja.env = env
    return get_jinja.env


def get_html(src_dir, ctx):
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
        path = src_dir
    else:
        html = None
        path = src_dir + ctx['url'] + 'index.html'
        template = ctx.get('template') or '_theme/base.tpl'
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
        for path in os.listdir(build_dir):
            path = os.path.join(build_dir, path)
            if os.path.isdir(path):
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
    save_urls(pages, os.path.join(src_dir, 'urls.json'))
    check_xml(pages)
    print(' * Build successful')
    return urls


def check_xml(pages):
    for page in pages.values():
        if not page.html:
            continue

        try:
            data = re.sub('(?i)<(!DOCTYPE|\?xml).*?[^>]>', '', page.html)
            ET.fromstring('<root>%s</root>' % data)
        except ET.ParseError as e:
            print(' * WARN: {}: "{}"'.format(page.index_file, e))


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

    watcher = Thread(target=watch_files, args=(src_dir, build_dir))
    watcher.daemon = True
    watcher.start()

    os.chdir(build_dir)
    http.server.test(
        port=port, HandlerClass=http.server.SimpleHTTPRequestHandler
    )


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

    with open(os.path.join(SRC_DIR, 'urls.json'), 'br') as f:
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
    print('\n'.join(all_aliases))
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
    subs = parser.add_subparsers(title='commands')

    def cmd(name, **kw):
        s = subs.add_parser(name, **kw)
        s.set_defaults(cmd=name)
        s.arg = lambda *a, **kw: s.add_argument(*a, **kw) and s
        s.exe = lambda f: s.set_defaults(exe=f) and s
        return s

    cmd('run', help='start dev server')\
        .arg('--no-build', action='store_true')\
        .arg('--port', type=int, default=5000)\
        .exe(lambda a: run(SRC_DIR, BUILD_DIR, a.no_build, a.port))

    cmd('build', help='build static content from `data` directory')\
        .arg('-b', '--bdir', default=BUILD_DIR, help='build directory')\
        .arg('-n', '--nginx-file', help='file nginx rules')\
        .arg('--port', type=int, default=8000)\
        .exe(lambda a: build(SRC_DIR, a.bdir, a.nginx_file))

    cmd('test_urls', help='test url responses')\
        .arg('-v', '--verbose', action='store_true')\
        .arg('--host', help='use host for test')\
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
