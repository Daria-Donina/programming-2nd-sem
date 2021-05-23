import re

import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    # print(parser)
    links = parser.findAll('a', 'storylink')
    subtexts = parser.findAll('td', 'subtext')

    for link, subtext in zip(links, subtexts):
        # author
        author = subtext.a.text

        link_comment = subtext.find('a', string=re.compile('comment'))
        comments = link_comment.text.split('\xa0')[0] if link_comment else '0'

        points = subtext.span.text.split(' ')[0]

        title = link.text

        url = link['href']
        news_list.append({
            'author': author,
            'comments': int(comments),
            'points': int(points),
            'title': title,
            'url': url
        })

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

get_news("https://news.ycombinator.com/newest")