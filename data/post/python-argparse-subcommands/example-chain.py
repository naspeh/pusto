#!/usr/bin/env python
import argparse


def run_test(module, settings=None):
    pass


def run_server(host, port, no_reload=False, settings=None):
    pass


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='app')
    cmds = parser.add_subparsers(help='commands')

    def cmd(name, **kw):
        p = cmds.add_parser(name, **kw)
        p.set_defaults(cmd=name)
        p.arg = lambda *a, **kw: p.add_argument(*a, **kw) and p
        p.exe = lambda f: p.set_defaults(exe=f) and p

        # global options
        p.arg('-s', '--settings', help='application settings')
        return p

    cmd('run', help='start dev server')\
        .arg('-P', '--port', type=int, default=8000, help='server port')\
        .arg('-H', '--host', default='localhost', help='server host')\
        .arg('--no-reload', action='store_true', help='without reloading')\
        .exe(lambda a: (
            run_server(a.host, a.port, a.no_reload, settings=a.settings)
        ))

    cmd('test', aliases=['t', 'te'], help='run tests')\
        .arg('target', default='.', nargs='?', help='python module or file')\
        .exe(lambda a: run_test(a.target, settings=a.settings))

    args = parser.parse_args(args)
    if not hasattr(args, 'exe'):
        parser.print_usage()
    else:
        args.exe(args)


if __name__ == '__main__':
    parse_args()
