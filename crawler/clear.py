#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import os
import glob
import log
import argparse


HTML_ROOT = 'articles/html/'
ARTICLE_ROOT = 'articles/text/'
HTML_EXTENSION = '.html'
TXT_EXTENSION = '.txt'

def parse_argument():
    parser = argparse.ArgumentParser(
        prog='clear',
        description="parse articles's htmls",
    )


    parser.add_argument(
        '--log',
        help='log level',
        default='error',
        choices=['critical', 'error', 'debug'],
        dest='log_level'
    )

    return parser.parse_args()


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_article_tag = False
        self.in_p_tag = False
        self._article = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.in_article_tag = True
        if tag == 'p':
            self.in_p_tag = True

    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article_tag = False
        if tag == 'p':
            self.in_p_tag = False

    def handle_data(self, data):
        if self.in_article_tag and self.in_p_tag and not data.strip() == '':
            self._article += data.strip() + '\n'

    def parse(self, page):
        self.feed(page)
        return self._article


def clear_page(page):
    return Parser().parse(page)


def clear():
    for file in glob.glob(HTML_ROOT + '?*.html'):
        filename = file[file.rfind('/') + 1:file.rfind('.')]
        file_path = HTML_ROOT + filename + HTML_EXTENSION
        article_path = ARTICLE_ROOT + filename + TXT_EXTENSION
        if not os.path.isfile(article_path):
            with open(file_path, 'r') as html:
                page = html.read()
            log.debug('Clear {filename}')
            article_text = clear_page(page)
            article = open(article_path, 'w')
            article.write(article_text)
            article.close()

def main():
    args = parse_argument()
    log.config(log.level(args.log_level))
    try:
        clear()
    except Exception as e:
        log.critical("Clear error occured: " + e)

if __name__ == '__main__':
    main()