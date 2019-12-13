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
        'access_token': '88f75997b99ee6047267a4159fa63f7a9a2915ee644ed79af54b495092d309f4d4ec1537203ec8d9ebc43',
        'v': '5.103'
    }
    domain = "https://api.vk.com/method"
    url = "{}/friends.get".format(domain)
    response = get(url, params=query_params)
    return response.json()
