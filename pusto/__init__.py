import os
import shutil

from werkzeug.exceptions import abort
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from . import data


def build(src_dir, build_dir):
    '''Build static site from `src_dir`'''
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    for ctx in data.get_urls(build_dir).values():
        if not ctx.index_file.endswith('.html'):
            with open(ctx.path, '+w') as f:
                f.write(ctx.html)


def create_app(src_dir):
    '''Create WSGI application'''
    urls = dict(data.get_urls(src_dir))

    @Request.application
    def app(request):
        if request.path in urls:
            ctx = urls[request.path]
            return Response(ctx.html, mimetype='text/html')

        abort(404)
    return app


def run_server(host, port, src_dir):
    '''Dev server with reloader'''
    run_simple(
        host, port, create_app(src_dir),
        use_reloader=True, use_debugger=True,
        static_files={'': src_dir},
        extra_files=[src_dir + data.tpl_file]
    )
