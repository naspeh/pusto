import os
import re
from collections import namedtuple, OrderedDict
from configparser import ConfigParser

from jinja2 import Environment, FileSystemLoader

from .markup import rst

strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)
Page = namedtuple('Page', (
    'url children index_file meta_file path meta '
    'aliases created title html html_title html_body'
))

meta_files = {'meta.ini'}
index_files = {'index.rst', 'index.tpl', 'index.html'}
tpl_file = '/_theme/base.tpl'


def get_pages(src_dir):
    tree = OrderedDict((f[0], (f[1], f[2])) for f in os.walk(src_dir))
    paths = list(tree.keys())
    paths.reverse()

    pages = OrderedDict()
    for path in paths:
        url = path.replace(src_dir, '') + '/'
        if not os.path.isdir(path):
            continue

        files = set(tree[path][1])
        index = (index_files & files or {None}).pop()
        meta = (meta_files & files or {None}).pop()
        children = [(k, v) for k, v in pages.items() if k.startswith(url)]
        children.reverse()
        children = OrderedDict(children)
        if index or children:
            ctx = get_html(src_dir, dict(
                url=url, children=children,
                index_file=index and url + index,
                meta_file=meta and url + meta
            ))
            pages[url] = ctx

    return pages


def get_meta(path):
    with open(path, 'r') as f:
        meta = f.read()
    parser = ConfigParser()
    parser.read_string('[default]\n' + meta)
    meta = dict(parser.items('default'))
    if 'aliases' in meta:
        meta['aliases'] = meta['aliases'].strip('\n').split('\n')
    return meta


def get_jinja(src_dir):
    if not hasattr(get_jinja, 'env'):
        get_jinja.env = Environment(loader=FileSystemLoader(src_dir))
    return get_jinja.env


def get_html(src_dir, ctx):
    env = get_jinja(src_dir)

    meta = get_meta(src_dir + ctx['meta_file']) if ctx['meta_file'] else {}
    meta.update(ctx)

    ctx.update(
        aliases=meta.get('aliases', None),
        title=meta.get('title', None),
        created=meta.get('created', None),
        html_title=None,
        html_body=None
    )

    if not ctx['index_file']:
        tpl = env.get_template('_theme/list.tpl')
        html = tpl.render(meta=meta)
    else:
        path = src_dir + ctx['index_file']
        with open(path) as f:
            text = f.read()

        if path.endswith('.html'):
            html = text

        elif path.endswith('.tpl'):
            tpl = env.get_template(ctx['index_file'])
            html = tpl.render(meta=meta)

        elif path.endswith('.rst'):
            title, body = rst(text, source_path=path)
            ctx.update(
                title=strip_tags(title),
                html_title=title,
                html_body=body,
                meta=meta
            )
            tpl = env.get_template(tpl_file)
            html = tpl.render(ctx)

    path = ctx['url'] + 'index.html'
    ctx.update(html=html, path=path, meta=meta)
    return Page(**ctx)
