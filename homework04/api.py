import requests
import time
import random
import config
import json


def get(url, params={}, timeout=5, max_retries=10, backoff_factor=0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    retry = 0
    while retry < max_retries:
        try:
            response = requests.get(url, params=params, timeout=timeout)
            # all ok
            return response
        except requests.exceptions.ReadTimeout:
            # error happened
            time.sleep(timeout)
            # calculate new timeout
            timeout = timeout * backoff_factor
            jetter = random.randint(0,1)
            timeout = timeout + timeout * jetter
            retry += 1


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    # with open("config.json") as config:
    #    con = json.load(config)
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'user_id': user_id,
        'fields': fields,
        'access_token': 'fd5f80e811feca5e357a2c9d7a42f1ca80c8295abed6d095885277550225a79a5111532334488b19268a4',
        'v': '5.103'
    }
    domain = "https://api.vk.com/method"
    url = "{}/friends.get".format(domain)
    response = get(url, params=query_params)
    return response.json()


def get_wall(
    owner_id: str ='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
):
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
        'access_token': 'aabaec7324040a5b1182778e7c2015d7c467b120bd4fda7895a81137547db7585c706200587c0f671a39a',
        'v': '5.103'
    }
    if count <= 100:
        domain = "https://api.vk.com/method"
        url = "{}/wall.get".format(domain)
        response = get(url, params=query_params).json()
        items_list = response['response']['items']
        post_list = []
        for item in items_list:
            try:
                post_list.append(item['text'])
                print(item['text'])
            except UnicodeError:
                pass
        return post_list
    else:
        code = """ var count = 2433;
        var posts = [];
        while (count > 100){
            return API.wall.get({
                "owner_id": "",
                "domain": "",
                "offset": 0,
                "count": 100,
                "filter": "owner",
                "extended": 0,
                "fields": "",
                "v": "5.103"
            });
            count = count - 100;
        }
        """
        post_list = requests.post(
            url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": query_params['access_token'],
                "v": "5.103"
            }
        ).json()
        print(post_list)
        count = count % 100
        post_list.append(get_wall(owner_id, domain, offset, count,
            filter, extended, fields, v))
