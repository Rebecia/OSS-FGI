#!/usr/bin/env python

from __future__ import print_function

import sys
import os

if sys.version_info[0] != 3:
    print('\n*** WARNING *** Please use Python 3! Exiting.')
    exit(1)


def main(config: str = '.lzrule.yaml'):
    try:
        # parse command line args
        from audit.options import Options
        opts = Options(sys.argv[1:])
        assert opts, 'Failed to parse cmdline args!'

        args = opts.args()
        assert args, 'Failed to get cmdline args!'

        # version request
        if args.ver and not args.cmd:
            from audit import __version__
            print(__version__)
            exit(1)

        # configuration file
        if not os.path.exists(config):
            config = os.path.expanduser(os.path.join('~', f'{config}'))
        assert os.path.exists(config), f'No {config} file found'

        # audit request
        if args.cmd == 'audit-online' or args.cmd == 'audit-offline':
            from audit.main import main
            main(args, config)


    except Exception as e:
        print(str(e))
        exit(1)
