import os
import shutil

from werkzeug.exceptions import abort
from werkzeug.serving import run_simple
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

from .data import get_pages, get_jinja


def build(src_dir, build_dir):
    '''Build static site from `src_dir`'''
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    for ctx in get_pages(build_dir).values():
        if not ctx.index_file.endswith('.html'):
            with open(ctx.path, '+w') as f:
                f.write(ctx.html)


def create_app(src_dir):
    '''Create WSGI application'''
    pages = get_pages(src_dir)
    urls = []
    for url, page in pages.items():
        urls += [(url, Response(page.html, mimetype='text/html'))]
        if page.aliases:
            urls += [(a, redirect(url)) for a in page.aliases]
    urls = dict(urls)

    @Request.application
    def app(request):
        response = urls.get(request.path, None)
        if response:
            return response

        abort(404)
    return app


def run_server(host, port, src_dir):
    '''Dev server with reloader'''
    extra_files = [
        os.path.join(src_dir, f)
        for f in get_jinja(src_dir).list_templates()
    ]
    run_simple(
        host, port, create_app(src_dir),
        use_reloader=True, use_debugger=True,
        static_files={'': src_dir},
        extra_files=extra_files
    )
