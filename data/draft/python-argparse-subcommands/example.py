#!/usr/bin/env python
import argparse


def run_test(module, settings=None):
    pass


def run_server(host, port, no_reload=False, settings=None):
    pass


def parse_args(args=None):
    parser = argparse.ArgumentParser(prog='app')
    subparsers = parser.add_subparsers(help='commands')

    cmd_run = subparsers.add_parser('run', help='start dev server')
    cmd_run.add_argument('-s', '--settings', help='application settings')
    cmd_run.add_argument(
        '-P', '--port', type=int, default=8000, help='server port'
    )
    cmd_run.add_argument(
        '-H', '--host', default='localhost', help='server host'
    )
    cmd_run.add_argument(
        '--no-reload', action='store_true', help='without reloading'
    )
    cmd_run.set_defaults(func=lambda a: (
        run_server(a.host, a.port, a.no_reload, settings=a.settings)
    ))

    cmd_test = subparsers.add_parser(
        'test', aliases=['t', 'te'], help='run tests'
    )
    cmd_test.add_argument('-s', '--settings', help='application settings')
    cmd_test.add_argument('target', default='.', help='python module or file')
    cmd_test.set_defaults(
        func=lambda a: run_test(a.module, settings=a.settings)
    )

    args = parser.parse_args(args)
    if not hasattr(args, 'func'):
        parser.print_usage()
    else:
        args.func(args)


if __name__ == '__main__':
    parse_args()
