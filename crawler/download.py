#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen
import os.path

FILE_ROOT = 'articles/html/'
HTML_EXTENSION = '.html'


def get_page_text(link):
    try:
        result = urlopen(link)
    except:
        print("Error occurred")
    else:
        if result.getcode() == 200:
            page_text = result.read().decode('utf-8')
            return page_text


def download(urls):
    if urls:
        links = urls
    else:
        with open('links.txt', 'r') as lines:
            links = lines.read().split('\n')
    for link in links:
        file_name = link[link.rfind('/') + 1:]
        print('Downloading ' + file_name + '...')
        file_name += HTML_EXTENSION
        file_path = FILE_ROOT + file_name
        if not os.path.isfile(file_path):
            page_text = get_page_text(link)
            with open(file_path, 'w') as html:
                html.write(page_text)
    lines.close()
    html.close()
    print('done')
