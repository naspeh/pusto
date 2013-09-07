#!/usr/bin/env python
from argparse import ArgumentParser
from multiprocessing import Process
from subprocess import call


serve = lambda: call('python2 -m SimpleHTTPServer 8000 0.0.0.0', shell=True)
watch = lambda: call(
    'watch rst2s5.py '
    '   --keep-theme-files '
    '   --current-slide '
    '   --visible-controls '
    '   text-v2.rst index.html',
    shell=True
)


def run_all():
    procs = [Process(target=t) for t in [serve, watch]]
    for p in procs:
        p.start()

    for p in procs:
        p.join()

    exit(int(any(p.exitcode for p in procs)))


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--watch', '-w', action='store_true', default=False)
    parser.add_argument('--serve', '-s', action='store_true', default=False)
    parser.add_argument('--all', '-a', action='store_true', default=False)
    args = parser.parse_args()
    try:
        if args.watch:
            watch()
        elif args.serve:
            serve()
        elif args.all:
            run_all()
        else:
            print(parser.format_help())
    except KeyboardInterrupt:
        exit()
