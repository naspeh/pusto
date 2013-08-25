import os
import re
from collections import namedtuple, OrderedDict
from configparser import ConfigParser

from jinja2 import Template, Environment, FileSystemLoader

from .markup import rst

meta_files = {'meta.ini'}
index_files = {'index.rst', 'index.tpl', 'index.html'}
tpl_file = '/_theme/base.tpl'
strip_tags = lambda t: t and re.sub(r'<.*?[^>]>', '', t)
UrlCtx = namedtuple('UrlContext', 'url child_urls index meta')


def get_urls(src_dir):
    tree = OrderedDict((f[0], (f[1], f[2])) for f in os.walk(src_dir))

    urls = OrderedDict()
    for path in tree:
        url = path.replace(src_dir, '') + '/'
        if not os.path.isdir(path):
            continue

        files = set(tree[path][1])
        index = (index_files & files or {None}).pop()
        if index:
            meta = (meta_files & files or {None}).pop()
            urls[url] = UrlCtx(
                url=url, child_urls=[],
                index=index and url + index,
                meta=meta and url + meta
            )
            parent = url
            for i in range(parent.count('/') - 1):
                parent = parent.rsplit('/', 2)[0] + '/'
                if parent in urls:
                    urls[parent].child_urls.append(url)
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

    with open(path) as f:
        text = f.read()

    meta = get_meta(build_dir + ctx.meta) if ctx.meta else {}
    meta.update(ctx._asdict())

    if path.endswith('.tpl'):
        env = Environment(loader=FileSystemLoader(build_dir))
        tpl = env.get_template(path.replace(build_dir, ''))
        html = tpl.render(meta=meta)
    elif path.endswith('.rst'):
        if not hasattr(get_html, 'tpl_cache'):
            with open(build_dir + tpl_file) as f:
                get_html.tpl_cache = f.read()
        tpl = get_html.tpl_cache

        title, body = rst(text, source_path=path)
        meta.update(
            title=strip_tags(title),
            html_title=title,
            html_body=body
        )
        html = Template(tpl).render(meta)

    path = path.rstrip('rst') + 'html'
    return path, html
