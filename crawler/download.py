#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.error import URLError
import os.path
import log
import datetime
import argparse

HTML_ROOT = 'articles/html/'
HTML_EXTENSION = '.html'

def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%y').date()


def parse_argument():
    parser = argparse.ArgumentParser(
        prog='download',
        description="Downloads articles's htmls",
        prefix_chars='--'
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
        default='critical',
        choices=['critical', 'error', 'debug'],
        dest='log_level'
    )

    return parser.parse_args()


def get_page_text(link):
    try:
        result = urlopen(link, timeout=10)
    except URLError:
        log.error("Url error occurred with " + link)
    else:
        if result.getcode() == 200:
            page_text = result.read().decode('utf-8')
            return page_text
        elif result.getcode() == 404:
            log.error('Page not found')
        else:
            log.debug(result.getcode() + ' code')


def download(urls):
    if urls:
        links = urls
    else:
        with open('links.txt', 'r') as lines:
            links = lines.read().rstrip().split('\n')
        lines.close()
    for link in links:
        file_name = link[link.rfind('/') + 1:]
        file_name += HTML_EXTENSION
        file_path = HTML_ROOT + file_name
        if not os.path.isfile(file_path):
            log.debug('Downloading ' + file_name + '...')
            page_text = get_page_text(link)
            if(page_text != None):
                with open(file_path, 'w') as html:
                    html.write(page_text)
                html.close()
        else:
            log.debug('Already downloaded ' + file_name)
    log.debug('done')


def main():
    args = parse_argument()
    log.config(log.level(args.log_level))
    log.debug('running download with ' + args.log_level + ' logging level')
    download(args.urls)


if __name__ == '__main__':
    main()