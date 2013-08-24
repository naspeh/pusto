import os
import re
from collections import namedtuple
from configparser import ConfigParser

from jinja2 import Template

from .markup import rst

tpl_file = '/_theme/index.tpl'
strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)
Ctx = namedtuple('UrlContext', 'url index meta')


def get_urls(src_dir):
    tree = dict((f[0], (f[1], f[2])) for f in os.walk(src_dir))

    def build_subdir(base_path):
        urls = []
        for item in tree[base_path][0]:
            path = '/'.join([base_path, item])
            url = path.replace(src_dir, '') + '/'
            if not os.path.isdir(path):
                continue

            urls += build_subdir(path)

            files = set(tree[path][1])
            index = ({'index.rst', 'index.html'} & files or {None}).pop()
            if index:
                meta = ({'meta.ini'} & files or {None}).pop()
                urls += [(url, Ctx(
                    url=url,
                    index=index and url + index,
                    meta=meta and url + meta
                ))]
        return urls

    urls = build_subdir(src_dir)
    return urls


def get_meta(path):
    with open(path, 'r') as f:
        meta = f.read()
    parser = ConfigParser()
    parser.read_string('[default]\n' + meta)
    meta = dict(parser.items('default'))
    if 'aliases' in meta:
        meta['aliases'] = meta['aliases'].strip('\n').split('\n')
    return meta


def get_html(ctx, build_dir):
    path = build_dir + ctx.index
    if path.endswith('.html'):
        return path, None

    if not hasattr(get_html, 'tpl_cache'):
        with open(build_dir + tpl_file) as f:
            get_html.tpl_cache = f.read()
    tpl = get_html.tpl_cache

    with open(path) as f:
        title, body = rst(f.read(), source_path=path)

    meta = get_meta(build_dir + ctx.meta) if ctx.meta else {}
    meta.update(
        url=ctx.url,
        title=strip_tags(title),
        html_title=title,
        html_body=body
    )
    html = Template(tpl).render(meta)
    path = path.rstrip('rst') + 'html'
    return path, html
