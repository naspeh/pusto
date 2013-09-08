import datetime as dt
import json
import os
import re
from collections import namedtuple, OrderedDict
from xml.etree import ElementTree as ET

from jinja2 import Environment, FileSystemLoader

from . import markup

Page = namedtuple('Page', (
    'url children index_file meta_file markup path '
    'aliases published hidden template title summary body html'
))

meta_files = ['meta.json']
index_files = ['index.' + t for t in 'html tpl rst md'.split(' ')]


def get_urls(src_dir):
    pages = get_pages(src_dir)
    urls = []
    for url, page in pages.items():
        if page.html:
            urls += [(url, page)]
            aliases = page.aliases or []
            aliases += [
                a.rstrip('/') for a in (aliases + [url]) if a.rstrip('/')
            ]
            aliases = set(aliases)
            urls += [(a, page) for a in aliases]
    return urls


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
        meta = ([f for f in meta_files if f in files] or [None])[0]
        index = ([f for f in index_files if f in files] or [None])[0]
        children = [
            (k, v) for k, v in pages.items()
            if k.rsplit('/', 2)[0] + '/' == url and not v.hidden
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
            markup=index and index.rsplit('.', 1)[1]
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

    if 'published' in meta:
        meta['published'] = dt.datetime.strptime(meta['published'], '%d.%m.%Y')

    keys = 'published aliases hidden template summary title body'.split(' ')
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
        path = src_dir + index_file
        with open(path, 'br') as f:
            text = f.read().decode()

        if ctx['markup'] == 'html':
            html = text
            bind_meta(ctx, html, method='html')

        elif ctx['markup'] == 'tpl':
            tpl = env.get_template(index_file)
            html = tpl.render(ctx)
            bind_meta(ctx, html, method='html')

        elif ctx['markup'] == 'md':
            body = markup.markdown(text)
            bind_meta(ctx, body, method='html')
            ctx.update(body=body)
            tpl = env.get_template('/_theme/base.tpl')
            html = tpl.render(ctx)

        elif ctx['markup'] == 'rst':
            title, body = markup.rst(text, source_path=path)
            bind_meta(ctx, body, method='html')
            if title:
                ctx['title'] = title
            ctx['body'] = body

            tpl = ctx.get('template', None) or '/_theme/base.tpl'
            tpl = env.get_template(tpl)
            html = tpl.render(ctx)

        path = src_dir + ctx['url'] + 'index.html'

    ctx.update(html=html, path=path)
    return Page(**ctx)
