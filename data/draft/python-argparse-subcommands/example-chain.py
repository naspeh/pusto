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
        s = cmds.add_parser(name, **kw)
        s.set_defaults(cmd=name)
        s.arg = lambda *a, **kw: s.add_argument(*a, **kw) and s
        s.exe = lambda f: s.set_defaults(exe=f) and s

        s.arg('-s', '--settings', help='application settings')
        return s

    cmd('run', help='start dev server')\
        .arg('-P', '--port', type=int, default=8000, help='server port')\
        .arg('-H', '--host', default='localhost', help='server host')\
        .arg('--no-reload', action='store_true', help='without reloading')\
        .exe(lambda a: (
            run_server(a.host, a.port, a.no_reload, settings=a.settings)
        ))

    cmd('test', aliases=['t', 'te'], help='run tests')\
        .arg('target', default='.', help='python module or file')\
        .exe(lambda a: run_test(a.module, settings=a.settings))

    args = parser.parse_args(args)
    if not hasattr(args, 'exe'):
        parser.print_usage()
    else:
        args.exe(args)


if __name__ == '__main__':
    parse_args()
