import os
import shutil

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

from .data import get_pages, get_jinja


def build(src_dir, build_dir):
    '''Build static site from `src_dir`'''
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    for ctx in get_pages(build_dir).values():
        if ctx.index_file and not ctx.index_file.endswith('.html'):
            with open(ctx.path, '+w') as f:
                f.write(ctx.html)


def create_app(src_dir, debug=False):
    '''Create WSGI application'''
    def get_urls():
        if not hasattr(get_urls, 'urls') or debug:
            pages = get_pages(src_dir)
            urls = []
            for url, page in pages.items():
                if page.html:
                    urls += [(url, Response(page.html, mimetype='text/html'))]
                    aliases = page.aliases or []
                    aliases += [
                        a.rstrip('/') for a in (aliases + [url])
                        if a.rstrip('/')
                    ]
                    aliases = set(aliases)
                    urls += [(a, redirect(url)) for a in aliases]
            get_urls.urls = dict(urls)
        return get_urls.urls

    @Request.application
    def app(request):
        if debug:
            get_jinja(src_dir).cache.clear()

        urls = get_urls()
        response = urls.get(request.path, None)
        if response:
            return response

        return NotFound()
    return app
