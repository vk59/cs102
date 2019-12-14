import pandas as pd
import requests
import textwrap

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm
from api import get

def get_wall(
    owner_id: str ='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
"""
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get 

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    # with open("config.json") as config:
    #    con = json.load(config)
    query_params = {
        'owner_id': owner_id,
        'domain': domain,
        'offset': offset,
        'count': count,
        'filter': filter,
        'extended': extended,
        'fields': fields,
        'access_token': 'fd5f80e811feca5e357a2c9d7a42f1ca80c8295abed6d095885277550225a79a5111532334488b19268a4',
        'v': '5.103'
    }
    domain = "https://api.vk.com/method"
    url = "{}/wall.get".format(domain)
    response = get(url, params=query_params)
    item_list = response['response']['items']
    post_list = []
    for item in item_list:
        post_list.append(item['text'])
    return post_list