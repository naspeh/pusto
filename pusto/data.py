import os
import re
import shutil

from .markup import rst


def build(src_dir, build_dir):
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.mkdir(build_dir)
    build_html(src_dir, build_dir)


def build_html(src_dir, build_dir):
    fs_tree = {}
    for f in os.walk(src_dir):
        fs_tree[f[0]] = f[1], f[2]

    root = fs_tree[src_dir]
    for item in root[0]:
        if not re.match('[a-z-A-Z0-9][a-zA-Z0-9-]*', item):
            continue
        src_path = '/'.join([src_dir, item])
        files = fs_tree[src_path][1]
        if not files or 'index.rst' not in files:
            continue

        path = build_dir
        parts = item.split('--')
        for part in parts[:-1]:
            if part:
                path = '/'.join([path, part])
                if not os.path.exists(path):
                    os.mkdir(path)
        path = '/'.join([path, parts[-1]])
        shutil.copytree(src_path, path)
        index = '/'.join([path, 'index.'])
        with open(index + 'rst') as f:
            text = rst(f.read(), source_path=index + 'rst')
        with open(index + 'html', '+w') as f:
            f.write(text)
