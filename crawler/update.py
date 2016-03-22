#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
from urllib.request import urlopen
from html.parser import HTMLParser
from datetime import date, datetime


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
            #print(data)
            cur_date = datetime.strptime(str(data), '%d.%m.%Y').date()
            link = {'link': self.link, 'title': self._title, 'date': cur_date}
            self._links.append(link)

    def parse(self, page):
        self.feed(page)
        return self._links


def get_urls(page):
    return GetUrls().parse(page)


VC_ARCHIVE_ROOT = "https://vc.ru/paper/archive/"


def check_for_date(list_of_links, from_date, to_date):
    new_list = list()
    for link in list_of_links:
        if from_date <= link['date'] <= to_date:
            new_list.append(link)
    return new_list


def update(from_date, to_date, output):
    list_of_links = list()
    cur_date = from_date
    print('wait...')
    while cur_date.month <= to_date.month or cur_date.year < to_date.year:
        print('Downloading data for', cur_date, "...")
        link_suffix = str(cur_date.year) + '/' + str(cur_date.month // 10) + str(cur_date.month % 10)
        link = VC_ARCHIVE_ROOT + link_suffix
        month_page = urlopen(link)
        month_page_text = month_page.read().decode('utf-8')
        list_of_links = list_of_links + get_urls(month_page_text)

        list_of_links = check_for_date(list_of_links, from_date, to_date)

        temp = cur_date.month

        if temp == 12:
            cur_date = date(cur_date.year + 1, temp % 12 + 1, cur_date.day)
        else:
            cur_date = date(cur_date.year, temp % 12 + 1, cur_date.day)

    with open('links.txt', 'w') as links:
        for link in list_of_links:
            links.write(link['link'] + '\n')
    links.close()

    print('done')
    if output:
        print('Articles: ')
        for link in list_of_links:
            print(link['link'], link['title'])
