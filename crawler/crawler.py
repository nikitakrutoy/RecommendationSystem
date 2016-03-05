import argparse
from urllib.request import urlopen
import sys
from html.parser import HTMLParser
from datetime import date, datetime


def make_date(string):
    return datetime.strptime(string, '%d-%m-%y').date()

def parse_argument(argv):
    parser = argparse.ArgumentParser(
        prog='crawler',
        description='Downloads articles from vc.ru',
        prefix_chars='--'
    )
    # creates subparsers object
    subparsers = parser.add_subparsers(dest = 'command')
    # creates update sub-parser
    parser_update = subparsers.add_parser(
        'update',
        description='update links',
        help='parser for update command',
        prefix_chars='--'
    )
    parser_update.add_argument(
        '--from',
        type=make_date,
        default = date.today(),
        dest='from_date',
        help='sets from which date to update links in format ' + date.today().strftime('%d-%m-%y')
    )
    parser_update.add_argument(
        '--to',
        type=make_date,
        default = date.today(),
        dest='to_date',
        help='sets to which date to update links in format '+ date.today().strftime('%d-%m-%y')
    )
    parser_update.add_argument(
        '--print',
        help='print updates links',
        action='store_true',
        dest='output'
    )
    return parser.parse_args();


class UpdateParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_ul_tag = False
        self.in_li_tag = False
        self.in_a_tag = False
        self.flag_for_date = False
        self.in_b_tag = False
        self.links = list()
        self.title = ''

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "ul":
            if 'class' in attrs and attrs['class'] == 'b-page-sitemap__articles':
                self.in_ul_tag = True
        if tag == 'li' and self.in_ul_tag:
            self.in_li_tag = True
        if tag == "a" and self.in_ul_tag and self.in_li_tag:
            if 'class' in attrs and attrs['class'] == 'title':
                self.in_a_tag = True
                self.flag_for_date = True
                self.link = attrs['href']
        if tag == "b" and self.in_ul_tag and self.in_li_tag and self.flag_for_date:
            self.in_b_tag = True

    def handle_endtag(self, tag):
        if tag == "ul":
            self.in_ul_tag = False
        if tag == "li":
            self.in_li_tag = False
        if tag == "a":
            self.in_a_tag = False
        if tag == "b":
            self.flag_for_date = False
            self.in_b_tag = False

    def handle_data(self, data):
        if self.in_a_tag:
            self.title = data
        if self.in_b_tag and self.flag_for_date:
            cur_date = data.split('.')
            cur_date = date(int(cur_date[2]), int(cur_date[1]), int(cur_date[0]))
            if self.from_date <= cur_date <= self.to_date:
                self.links.append([self.link, self.title])

    def parse(self, page, from_date, to_date):
        self.from_date = from_date
        self.to_date = to_date
        self.feed(page)
        return self.links


def update(args):

    from_date = args.from_date
    to_date = args.to_date
    output = args.output
    links = open('links.txt', 'w') # for now every update rewrites the list of saved links
    list_of_links = list()
    link_prefix = "https://vc.ru/paper/archive/"
    cur_date = from_date
    print('wait...')
    while cur_date.month <= to_date.month or cur_date.year < to_date.year:
        print('Downloading data for', cur_date, "...")
        link_suffix = str(cur_date.year) + '/' + str(cur_date.month // 10) + str(cur_date.month % 10)
        link = link_prefix + link_suffix
        month_page = urlopen(link)
        month_page_text = month_page.read().decode('utf-8')
        list_of_links = list_of_links + UpdateParser().parse(month_page_text, from_date, to_date)
        temp = cur_date.month
        if temp == 12:
            cur_date = date(cur_date.year + 1, temp % 12 + 1, cur_date.day)
        else:
            cur_date = date(cur_date.year, temp % 12 + 1, cur_date.day)

    with open('links.txt', 'w') as links:
        for link in list_of_links:
            links.write(link[0] + ' ' + link[1] + '\n')
    print('updated')
    if output:
        print('Articles: ')
        for link in list_of_links:
            print(link[0], link[1])


def download(args):
    return 0


def run_command(args):
    commands = {'update': update, 'download': download}
    commands[args.command](args)


def main():
    args = parse_argument(sys.argv)
    run_command(args)

if __name__ == '__main__':
    main()
