#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import os
import glob
import log


FILE_ROOT = 'articles/html/'
ARTICLE_ROOT = 'articles/text/'
HTML_EXTENSION = '.html'
TXT_EXTENSION = '.txt'


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
    article_text = ''
    for file in glob.glob(FILE_ROOT + '?*.html'):
        filename = file[file.rfind('/') + 1:file.rfind('.')]
        file_path = FILE_ROOT + filename + HTML_EXTENSION
        article_path = ARTICLE_ROOT + filename + TXT_EXTENSION
        if not os.path.isfile(article_path):
            with open(file_path, 'r') as html:
                page = html.read()
            log.debug('clearing ' + filename + '...')
            article_text = clear_page(page)
            article = open(article_path, 'w')
            article.write(article_text)
            html.close()
            article.close()
    log.debug('all cleared')