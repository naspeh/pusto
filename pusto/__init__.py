import os
import shutil

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

from .data import get_urls, get_jinja


def build(src_dir, build_dir, nginx_file=None):
    '''Build static site from `src_dir`'''
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    urls = get_urls(build_dir)
    nginx = {}
    for url, page in urls:
        if url != page.url and (url + '/') != page.url:
            nginx[url.rstrip('/')] = page.url
        elif page.index_file and not page.index_file.endswith('.html'):
            with open(page.path, 'bw') as f:
                f.write(page.html.encode())
    if nginx:
        lines = [
            'rewrite ^{}/?$ {} permanent;'.format(u, p)
            for u, p in nginx.items()
        ]
        lines = '\n'.join(lines)
        if not nginx_file:
            nginx_file = os.path.join(build_dir, '.nginx')

        with open(nginx_file, 'bw') as f:
            f.write(lines.encode())
    print('Build successful')
    return urls


def create_app(src_dir, build_dir, debug=False):
    '''Create WSGI application'''
    def _urls(reload=False):
        if not hasattr(_urls, 'cache') or reload:
            pages = build(src_dir,  build_dir)
            urls = []
            for url, page in pages:
                if url == page.url:
                    urls += [(url, Response(page.html, mimetype='text/html'))]
                else:
                    urls += [(url, redirect(page.url, 301))]
            _urls.cache = dict(urls)
        return _urls.cache

    get_jinja.debug = debug

    @Request.application
    def app(request):
        urls = _urls()
        if '__r' in request.args:
            get_jinja(build_dir).cache.clear()
            urls = _urls(reload=True)

        response = urls.get(request.path, None)
        if response:
            return response

        return NotFound()
    return app
