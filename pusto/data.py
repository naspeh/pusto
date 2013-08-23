import json
import os
import re
import string
from collections import namedtuple

from .markup import rst

strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)
Ctx = namedtuple('UrlContext', 'index meta')


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
                meta = ({'meta.json'} & files or {None}).pop()
                urls += [(url, Ctx(
                    index=index and url + index,
                    meta=meta and url + meta
                ))]
        return urls

    urls = build_subdir(src_dir)
    return urls


def get_html(ctx, build_dir):
    index = build_dir + ctx.index
    if index.endswith('.html'):
        return index, None

    if ctx.meta:
        with open(build_dir + ctx.meta, 'r') as f:
            meta = json.loads(f.read())
    else:
        meta = {}

    if not hasattr(get_html, 'tpl_cache'):
        with open(build_dir + '/_theme/index.tpl') as f:
            get_html.tpl_cache = f.read()
    tpl = get_html.tpl_cache

    with open(index) as f:
        title, body = rst(f.read(), source_path=index)

    meta.update(
        title=strip_tags(title),
        html_title=title,
        html_body=body
    )
    html = string.Template(tpl).substitute(meta)
    index = index.rstrip('rst') + 'html'
    return index, html
