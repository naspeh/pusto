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

    env = get_jinja(build_dir)
    nginx = {}
    for url, page in get_urls(build_dir):
        html = path = None
        if url != page.url and (url + '/') != page.url:
            nginx[url.rstrip('/')] = page.url
            path = build_dir + url.rstrip('/') + '/'
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                tpl = env.get_template('_theme/redirect.tpl')
                html = tpl.render(url=page.url)
                path = path + 'index.html'
        elif page.index_file and not page.index_file.endswith('.html'):
            html, path = page.html, page.path

        if html and path:
            with open(path, 'bw') as f:
                f.write(html.encode())
    if nginx:
        lines = [
            'rewrite .*{}/?$ http://$host{} permanent;'.format(u, p)
            for u, p in nginx.items()
        ]
        lines = '\n'.join(lines)
        if nginx_file:
            with open(nginx_file, 'bw') as f:
                f.write(lines.encode())
        else:
            print('Rules for nginx:')
            print(lines)


def create_app(src_dir, debug=False):
    '''Create WSGI application'''
    def _urls():
        if not hasattr(_urls, 'urls') or debug:
            pages = get_urls(src_dir)
            urls = []
            for url, page in pages:
                if url == page.url:
                    urls += [(url, Response(page.html, mimetype='text/html'))]
                else:
                    urls += [(url, redirect(page.url, 301))]
            _urls.urls = dict(urls)
        return _urls.urls

    @Request.application
    def app(request):
        if debug:
            get_jinja(src_dir).cache.clear()

        urls = _urls()
        response = urls.get(request.path, None)
        if response:
            return response

        return NotFound()
    return app
