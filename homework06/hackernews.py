from bottle import (
    route, run, template, request, redirect
)

from sqlalchemy import engine
from sqlalchemy import update
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    this_label = request.query.label
    this_id = request.query.id
    s = session()
    changing_news = s.query(News).get(this_id)
    changing_news.label = this_label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news_list = get_news("https://news.ycombinator.com/", n_pages=5)
    s = session()
    prev_news_list = s.query(News).all()
    for new in news_list:
        for prev_new in prev_news_list:
            if (new['title'] == prev_new.title and
                    new['author'] == prev_new.author):
                break
        else:
            this_new = News(title=new['title'],
                            author=new['author'],
                            url=new['url'],
                            comments=new['comments'],
                            points=new['points'])
            s.add(this_new)
            s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)

