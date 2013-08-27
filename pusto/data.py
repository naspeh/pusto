import datetime as dt
import json
import os
import re
from collections import namedtuple, OrderedDict

from jinja2 import Environment, FileSystemLoader

from .markup import rst

strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)
Page = namedtuple('Page', (
    'url children index_file meta_file path '
    'aliases published title html html_title html_body'
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
        if index or children:
            ctx = get_html(src_dir, dict(
                url=url, children=children,
                index_file=index and url + index,
                meta_file=meta and url + meta,
            ))
            pages[url] = ctx

    return pages


def bind_meta(ctx, meta, raw=True, parse=False):
    if parse:
        meta = re.search('(?s)<!--\s*META(\s*\{.*})\s*-->', meta)
        if meta:
            meta = meta.group(1)
        else:
            return

    if raw:
        meta = json.loads(meta)

    if 'published' in meta:
        meta['published'] = dt.datetime.strptime(meta['published'], '%d.%m.%Y')

    for key in ['published', 'aliases', 'title', 'html_title', 'html_body']:
        ctx.setdefault(key, None)
        if key in meta:
            ctx[key] = meta[key]


def get_jinja(src_dir):
    if not hasattr(get_jinja, 'env'):
        get_jinja.env = Environment(loader=FileSystemLoader(src_dir))
    return get_jinja.env


def get_html(src_dir, ctx):
    env = get_jinja(src_dir)

    if ctx['meta_file']:
        with open(src_dir + ctx['meta_file'], 'r') as f:
            meta = f.read()
        bind_meta(ctx, meta)
    else:
        bind_meta(ctx, {}, raw=False)

    if not ctx['index_file']:
        tpl = env.get_template('_theme/list.tpl')
        html = tpl.render(ctx)

    else:
        path = src_dir + ctx['index_file']
        with open(path) as f:
            text = f.read()

        if path.endswith('.html'):
            html = text
            bind_meta(ctx, html, parse=True)

        elif path.endswith('.tpl'):
            tpl = env.get_template(ctx['index_file'])
            html = tpl.render(ctx)
            bind_meta(ctx, html, parse=True)

        elif path.endswith('.rst'):
            title, body = rst(text, source_path=path)
            bind_meta(ctx, body, parse=True)
            ctx.update(
                title=strip_tags(title),
                html_title=title,
                html_body=body
            )
            tpl = env.get_template('/_theme/base.tpl')
            html = tpl.render(ctx)

    path = ctx['url'] + 'index.html'
    ctx.update(html=html, path=path)
    return Page(**ctx)
