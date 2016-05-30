from urllib.request import urlopen
from datetime import datetime
from urllib.error import URLError
import log


def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%y').date()

def load(link):
    try:
        result = urlopen(link, timeout=10)
    except URLError:
        log.error('Url error occurred with {link}')
    else:
        code = result.getcode();
        if code == 200:
            log.debug("Load " + link + " : " + str(code))
            page_text = result.read().decode('utf-8')
            return page_text
        else:
            log.debug("Load " + link + " : " + str(code))