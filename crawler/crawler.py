#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys

from datetime import date, datetime
from update import update
from download import download


def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%y').date()


def parse_argument(argv):
    parser = argparse.ArgumentParser(
        prog='crawler',
        description='Downloads articles from vc.ru',
        prefix_chars='--'
    )
    subparsers = parser.add_subparsers(dest = 'command', help = 'available commands')
    parser_update = subparsers.add_parser(
        'update',
        description='update links',
        help='updates links',
        prefix_chars='--'
    )
    parser_update.add_argument(
        '--from',
        type=str_to_date,
        default = date.today(),
        dest='from_date',
        help='start of interval to upload links(default date is today: ' + date.today().strftime('%d-%m-%y') + ')'
    )
    parser_update.add_argument(
        '--to',
        type=str_to_date,
        default = date.today(),
        dest='to_date',
        help='end of interval to upload links(default date is today: ' + date.today().strftime('%d-%m-%y') + ')'
    )
    parser_update.add_argument(
        '--print',
        help='print updated links',
        action='store_true',
        dest='output'
    )

    parser_download = subparsers.add_parser(
        'download',
        description='download html pages',
        help='download html pages',
    )

    parser_download.add_argument(
        'urls',
        type=str,
        nargs='*'
    )

    return parser.parse_args();


def main():
    args = parse_argument(sys.argv)
    command = args.command
    if command == 'update':
        update(args.from_date, args.to_date, args.output)
    elif command == 'download':
       download(args.urls)

if __name__ == '__main__':
    main()
