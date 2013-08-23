import os
import shutil

from werkzeug.exceptions import abort
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

from . import data


def build(src_dir, build_dir):
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    shutil.copytree(src_dir, build_dir)

    for url, ctx in data.get_urls(build_dir):
        index, html = data.get_html(ctx, build_dir)
        if not html:
            with open(index, '+w') as f:
                f.write(html)


def create_app(src_dir):
    urls = dict(data.get_urls(src_dir))

    @Request.application
    def app(request):
        if request.path == '/l/':
            html = [
                '<a href="{0}">{0}</a><br>'.format(u)
                for u in sorted(urls.keys())
            ]
            return Response(html, mimetype='text/html')

        elif request.path in urls:
            index, html = data.get_html(urls[request.path], src_dir)
            if not html:
                with open(index) as f:
                    html = f.read()
            return Response(html, mimetype='text/html')

        abort(404)
    return app


def run_server(host, port, src_dir):
    run_simple(
        host, port, create_app(src_dir), static_files={'': src_dir},
        use_reloader=True, use_debugger=True
    )
