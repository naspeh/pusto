import json
import os
import re
import shutil
import string

from .markup import rst

strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)


def build(src_dir, build_dir):
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    tree = {}
    for f in os.walk(build_dir):
        tree[f[0]] = f[1], f[2]

    with open(build_dir + '/_theme/index.html') as f:
        template = f.read()
    build_subdir(build_dir, tree, template=template)


def build_subdir(base_path, tree, template):
    for item in tree[base_path][0]:
        path = '/'.join([base_path, item])
        if not os.path.isdir(path):
            continue

        build_subdir(path, tree, template)

        files = tree[path][1]
        meta = {}
        if 'meta.json' in files:
            with open('/'.join([path, 'meta.json']), 'r') as f:
                meta = json.loads(f.read())

        title = body = None
        if 'index.rst' in files:
            index = '/'.join([path, 'index.'])
            with open(index + 'rst') as f:
                title, body = rst(f.read(), source_path=index + 'rst')

            html = string.Template(template).substitute(
                title=strip_tags(title),
                html_title=title,
                html_body=body
            )
            with open(index + 'html', '+w') as f:
                f.write(html)
