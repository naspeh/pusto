import datetime as dt
import json
import os
import re
from collections import namedtuple, OrderedDict
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader

from .markup import rst

strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)
Page = namedtuple('Page', (
    'url children index_file meta_file path '
    'aliases published title summary html html_title html_body'
))

meta_files = {'meta.json'}
index_files = {'index.rst', 'index.tpl', 'index.html'}


def get_pages(src_dir):
    tree = OrderedDict((f[0], (f[1], f[2])) for f in os.walk(src_dir))
    paths = list(tree.keys())
    paths.reverse()

    pages = OrderedDict()
    for path in paths:
        url = path.replace(src_dir, '') + '/'
        if not os.path.isdir(path) or url.rsplit('/', 2)[1].startswith('_'):
            continue

        files = set(tree[path][1])
        index = (index_files & files or {None}).pop()
        meta = (meta_files & files or {None}).pop()
        children = [
            (k, v) for k, v in pages.items()
            if k.rsplit('/', 2)[0] + '/' == url
        ]
        children.sort(
            key=lambda v: v[1].published and v[1].published.isoformat() or '',
            reverse=True
        )
        children = OrderedDict(children)
        ctx = get_html(src_dir, dict(
            url=url, children=children,
            index_file=index and url + index,
            meta_file=meta and url + meta,
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
        data = re.sub('(?i)<!DOCTYPE.*?[^>]>', '', data)
        root = ET.fromstring('<root>%s</root>' % data)
        summary = root.findall('*[@id="summary"]')
        if summary:
            summary = ET.tostring(summary[0], encoding='utf8', method='html')
            meta['summary'] = summary.decode()
    elif method == 'json':
        meta = json.loads(meta)

    if 'published' in meta:
        meta['published'] = dt.datetime.strptime(meta['published'], '%d.%m.%Y')

    keys = 'published aliases title summary html_title html_body'.split(' ')
    for key in keys:
        ctx.setdefault(key, None)
        if key in meta:
            ctx[key] = meta[key]


def get_jinja(src_dir):
    if not hasattr(get_jinja, 'env'):
        get_jinja.env = Environment(loader=FileSystemLoader(src_dir))
    return get_jinja.env


def get_html(src_dir, ctx):
    env = get_jinja(src_dir)

    meta_file = ctx['meta_file']
    if meta_file:
        with open(src_dir + meta_file, 'r') as f:
            meta = f.read()
        bind_meta(ctx, meta, method='json')
    else:
        bind_meta(ctx, {})

    index_file = ctx['index_file']
    if not index_file:
        path = src_dir
        html = None
    else:
        path = src_dir + index_file
        with open(path) as f:
            text = f.read()

        if index_file.endswith('.html'):
            html = text
            bind_meta(ctx, html, method='html')

        elif index_file.endswith('.tpl'):
            tpl = env.get_template(index_file)
            html = tpl.render(ctx)
            bind_meta(ctx, html, method='html')

        elif index_file.endswith('.rst'):
            title, body = rst(text, source_path=path)
            bind_meta(ctx, body, method='html')
            ctx.update(
                title=strip_tags(title),
                html_title=title,
                html_body=body
            )
            tpl = env.get_template('/_theme/base.tpl')
            html = tpl.render(ctx)

        path = src_dir + ctx['url'] + 'index.html'

    ctx.update(html=html, path=path)
    return Page(**ctx)
