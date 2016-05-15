#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os.path
import log
import argparse
from utils import load, str_to_date

HTML_ROOT = 'articles/html/'
HTML_EXTENSION = '.html'


def parse_argument():
    parser = argparse.ArgumentParser(
        prog='download',
        description="Downloads articles's htmls",
    )
    parser.add_argument(
        'urls',
        type=str,
        nargs='*',
        help='list of urls to download'
    )

    parser.add_argument(
        '--log',
        help='log level',
        default='error',
        choices=['critical', 'error', 'debug'],
        dest='log_level'
    )

    return parser.parse_args()



def download(links):
    for link in links:
        file_name = link[link.rfind('/') + 1:]
        file_name += HTML_EXTENSION
        file_path = HTML_ROOT + file_name
        if not os.path.isfile(file_path):
            page_text = load(link)
            if(page_text != None):
                with open(file_path, 'w') as html:
                    html.write(page_text)
        else:
            log.debug(file_name + ' is already downloaded')


def main():
    args = parse_argument()
    log.config(log.level(args.log_level))
    try:
        if args.urls:
            links = args.urls
        else:
            with open('links.txt', 'r') as lines:
                links = lines.read().rstrip().split('\n')
        download(links)
    except Exception as e:
        log.critical("Download error occured: {e}")


if __name__ == '__main__':
    main()