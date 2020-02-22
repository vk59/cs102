import requests
from bs4 import BeautifulSoup
import time
import random


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    tbl_list = parser.table.findAll('table')
    tr_list = tbl_list[1].findAll('tr')
    i = 0
    while (i < len(tr_list) - 3):
        this_new = dict() 
        a_title_list = tr_list[i].findAll('a')
        title = a_title_list[1].text
        url = a_title_list[1]['href']
        i += 1
        a_sub_list = tr_list[i].findAll('a')
        author = a_sub_list[0].text
        try:
            com_str = a_sub_list[3].text
            try:
                comments = int(com_str[:-9])
            except:
                if com_str[0] == '1':
                    comments = 1
                else:
                    comments = 0
        except:
            comments = 0
        try:
            p_str = tr_list[i].span.text
            points = int(p_str[:-7])
        except:
            points = 1
        i += 2
        this_new = {
            'title': title,
            'url': url,
            'author': author,
            'comments': comments,
            'points': points
        }
        news_list.append(this_new)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    tbl_list = parser.table.findAll('table')
    a_list = tbl_list[1].findAll('a')
    next_url = a_list[-1]['href']
    return next_url


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        timeout = 30*random.random()
        while response.status_code != 200:
            time.sleep(timeout)
            response = requests.get(url)
            timeout = timeout + 40*random.random()
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.append(news_list)
        n_pages -= 1
    return news

