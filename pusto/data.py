import json
import os
import pprint
import re
import shutil
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
            index = ({'index.html', 'index.rst'} & files or {None}).pop()
            if index:
                meta = ({'meta.json'} & files or {None}).pop()
                urls += [(url, Ctx(
                    index=index and url + index,
                    meta=meta and url + meta
                ))]
        return urls

    urls = build_subdir(src_dir)
    pprint.pprint(urls)
    return urls


def build(src_dir, build_dir):
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    with open(build_dir + '/_theme/index.html') as f:
        template = f.read()

    for url, ctx in get_urls(src_dir):
        if ctx.meta:
            with open(build_dir + ctx.meta, 'r') as f:
                meta = json.loads(f.read())
        else:
            meta = {}

        title = body = None
        if ctx.index.endswith('.rst'):
            index = build_dir + ctx.index
            with open(index) as f:
                title, body = rst(f.read(), source_path=ctx.index)

            meta.update(
                title=strip_tags(title),
                html_title=title,
                html_body=body
            )
            html = string.Template(template).substitute(meta)
            with open(index.rstrip('rst') + 'html', '+w') as f:
                f.write(html)
