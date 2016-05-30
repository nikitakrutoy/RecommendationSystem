#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from datetime import date, datetime
from utils import load, str_to_date

import log
import argparse


def parse_argument():
    parser = argparse.ArgumentParser(
        prog='update',
        description='update links',
    )

    parser.add_argument(
        '--log',
        help='log level',
        default='error',
        choices=['critical', 'error',  'debug'],
        dest='log_level'
    )

    parser.add_argument(
        '--from',
        type=str_to_date,
        default = date.today(),
        dest='from_date',
        help='start of interval to upload links(default date is today: ' + date.today().strftime('%d-%m-%y') + ')'
    )
    parser.add_argument(
        '--to',
        type=str_to_date,
        default = date.today(),
        dest='to_date',
        help='end of interval to upload links(default date is today: ' + date.today().strftime('%d-%m-%y') + ')'
    )
    parser.add_argument(
        '--print',
        help='prints updated links',
        action='store_true',
        dest='output'
    )
    return parser.parse_args()


class GetUrls(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._in_ul_tag = False
        self._in_li_tag = False
        self._in_a_tag = False
        self._flag_for_date = False
        self._in_b_tag = False
        self._links = list()
        self._title = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "ul":
            if 'class' in attrs and attrs['class'] == 'b-page-sitemap__articles':
                self._in_ul_tag = True
        if tag == 'li' and self._in_ul_tag:
            self._in_li_tag = True
        if tag == "a" and self._in_ul_tag and self._in_li_tag:
            if 'class' in attrs and attrs['class'] == 'title':
                self._in_a_tag = True
                self._flag_for_date = True
                self.link = attrs['href']
        if tag == "b" and self._in_ul_tag and self._in_li_tag and self._flag_for_date:
            self._in_b_tag = True

    def handle_endtag(self, tag):
        if tag == "ul":
            self._in_ul_tag = False
        if tag == "li":
            self._in_li_tag = False
        if tag == "a":
            self._in_a_tag = False
        if tag == "b":
            self._flag_for_date = False
            self._in_b_tag = False

    def handle_data(self, data):
        if self._in_a_tag:
            self._title = data
        if self._in_b_tag and self._flag_for_date:
            cur_date = datetime.strptime(str(data), '%d.%m.%Y').date()
            link = {'link': self.link, 'title': self._title, 'date': cur_date}
            self._links.append(link)

    def parse(self, page):
        self.feed(page)
        return self._links


def get_urls(page):
    return GetUrls().parse(page)


VC_ARCHIVE_ROOT = "https://vc.ru/paper/archive/"


def filter_with_date_interval(references, from_date, to_date):
    return [reference for reference in references if from_date <= reference['date'] <= to_date]

def date_range(from_date, to_date):
    while from_date.month <= to_date.month or from_date.year < to_date.year:
        yield from_date
        if from_date.month == 12:
            from_date = date(from_date.year + 1, from_date.month % 12 + 1, from_date.day)
        else:
            from_date = date(from_date.year, from_date.month % 12 + 1, from_date.day)

def update(from_date, to_date, output):
    references = list()
    for cur_date in date_range(from_date, to_date):
        log.debug('Load archive page: ' + str(cur_date))
        link_suffix = str(cur_date.year) + '/' + str(cur_date.month // 10) + str(cur_date.month % 10)
        link = VC_ARCHIVE_ROOT + link_suffix
        month_page_text = load(link)
        if (month_page_text != None):
            references = references + get_urls(month_page_text)
    references = filter_with_date_interval(references, from_date, to_date)
    with open('links.txt', 'w') as links:
        for link in references:
            links.write(link['link'] + '\n')

    if output:
        print('Articles: ')
        for link in references:
            print(link['link'])


def main():
    args = parse_argument()
    log.config(log.level(args.log_level))
    try:
        update(args.from_date, args.to_date, args.output)
    except Exception as er:
        log.critical('Update error occured: ' + er)


if __name__ == '__main__':
    main()
