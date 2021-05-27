from scraputils import get_news
from db import News, session


def initialize_db(n_pages):
    news = get_news("https://news.ycombinator.com/newest", n_pages)
    s = session()
    for dct in news:
        record = News(
            title=dct["title"],
            author=dct["author"],
            url=dct["url"],
            comments=dct["comments"],
            points=dct["points"],
        )

        print(dct)

        s.add(record)
        s.commit()


initialize_db(40)
