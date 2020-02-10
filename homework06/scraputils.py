import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    # PUT YOUR CODE HERE

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    tbl_list = parser.table.findAll('table')
    a_list = tbl_list[1].findAll('a')
    next_url = a_list[-1]
    return next_url


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(url)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

