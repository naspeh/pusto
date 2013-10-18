#!/usr/bin/env python
import argh


@argh.aliases('t', 'te')
def test(module, settings=None):
    '''run tests'''
    pass


def run(host='localhost', port=8000, no_reload=False, settings=None):
    '''run dev server'''
    pass

if __name__ == '__main__':
    argh.dispatch_commands([run, test])
