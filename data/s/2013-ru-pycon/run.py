#!/usr/bin/env python
import os
from argparse import ArgumentParser
from subprocess import call


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--watch', '-w', action='store_true', default=False)
    parser.add_argument('--serve', '-s', action='store_true', default=False)
    args = parser.parse_args()
    try:
        os.chdir(os.path.dirname(__file__))
        if args.watch:
            call(
                'watch rst2s5.py '
                '   --keep-theme-files '
                '   --current-slide '
                '   --visible-controls '
                '   index.rst index.html',
                shell=True
            )

        elif args.serve:
            call('python2 -m SimpleHTTPServer 8000 0.0.0.0', shell=True)

        else:
            print(parser.format_help())
    except KeyboardInterrupt:
        exit()
