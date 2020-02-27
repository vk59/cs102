from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

    def __init__(self, title, url, author, comments, points):
        self.title = title
        self.url = url
        self.author = author
        self.comments = comments
        self.points = points
        self.label = None


Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    s = session()
    news = get_news('https://news.ycombinator.com/news', n_pages=15)
    for post in news:
        p_title = post['title']
        p_url = post['url']
        p_author = post['author']
        p_comments = post['comments']
        p_points = post['points']
        post_db = News(
            title=p_title,
            url=p_url,
            author=p_author,
            comments=p_comments,
            points=p_points
    )
        s.add(post_db)
        s.commit()
