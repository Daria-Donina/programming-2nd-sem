from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    record = s.query(News).filter(News.id == request.query["id"]).first()
    record.label = request.query['label']
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    news = get_news('https://news.ycombinator.com/newest')

    s = session()
    for dct in news:
        entry = News(
            title=dct["title"],
            author=dct["author"],
            comments=dct["comments"],
            points=dct["points"],
            url=dct["url"],
        )

        records = s.query(News).filter(News.title == entry.title and News.author == entry.author).all()

        if len(records) == 0:
            s.add(entry)
            s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)
