#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen
import os.path
import log

FILE_ROOT = 'articles/html/'
HTML_EXTENSION = '.html'


def get_page_text(link):
    try:
        result = urlopen(link)
    except:
        log.error("Error occurred")
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
        file_path = FILE_ROOT + file_name
        if not os.path.isfile(file_path):
            log.debug('Downloading ' + file_name + '...')
            page_text = get_page_text(link)
            with open(file_path, 'w') as html:
                html.write(page_text)
            html.close()
        else:
            log.debug('Already downloaded ' + file_name)
    log.debug('all downloaded')
