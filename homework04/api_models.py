import requests
import pymorphy2

from api import get_wall

def normalize(posts_list):
    # убираем всё лишнее в посте
    i = 0
    new_posts = []
    for post in posts_list:
        new_posts.append(post)
        for ch in post:
            if not ('а' <= ch <= 'я' or 'А' <= ch <= 'Я' or ch == ' '):
                new_posts[i] = new_posts[i][:new_posts[i].index(ch)] +\
                    new_posts[i][new_posts[i].index(ch) + 1:]
        i += 1
    return new_posts
    # проводим нормализацию слов
    words = []
    morph = MorphAnalyzer()
    i = 0
    for post in new_posts:
        words.append(post.split())
        for word in words[i]:
            norm_word = morph.parse(word)[0].tag.POS
            word = norm_word
        i += 1
    return words

def topics_model(
    owner_id: str ='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
):
    post_list = get_wall(
        owner_id=owner_id,
        domain=domain,
        offset=offset,
        count=count,
        filter=filter,
        extended=extended,
        fields=fields,
        v=v
    )
