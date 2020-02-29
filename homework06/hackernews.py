from bottle import (
    route, run, template, request, redirect
)

import string
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
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=4)
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


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route('/recomendations')
def recomendations():
    s = session()
    all_data = []
    data = [[], []]
    length = s.query(News).count()
    for ID in range(1, length + 1):
        post = s.query(News).get(ID)
        all_data.append(post)
    for i in range(1, length):
        data[0].append(all_data[i].title)
        data[1].append(all_data[i].label)
    X, y = [], []
    for i in range(len(data[0])):
        X.append(data[0][i])
        y.append(data[1][i])
    X = [clean(x).lower() for x in X]
    model = NaiveBayesClassifier()
    part = len(X)*7 // 10
    X_train, y_train, X_test, y_test = X[:part], y[:part], X[part:], y[part:]
    model.fit(X_train, y_train)
    score=model.score(X_test, y_test)
    rec = NaiveBayesClassifier()
    rec.fit(X, y)
    rows = s.query(News).filter(News.label == None).all()
    X_new = []
    for row in rows:
        X_new.append(row.title)
    classified_news = rec.predict(X_new)
    return template('news_recomendations', rows=classified_news, score=score)


if __name__ == "__main__":
    run(host="localhost", port=8080)

