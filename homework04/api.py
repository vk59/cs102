import requests
import time
import random
import config
import json
import datetime


with open("access/config.json") as config:
    con = json.load(config)


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
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'user_id': user_id,
        'fields': fields,
        'access_token': con['access_token'],
        'v': '5.103'
    }
    domain = "https://api.vk.com/method"
    url = "{}/friends.get".format(domain)
    response = get(url, params=query_params)
    return response.json()


def age_predict(user_id):
    """
    >>> age_predict(???)
    ???
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    count_real_friends = -1
    sum_of_ages = -1
    friends = get_friends(user_id, fields='bdate')
    count_real_friends = 0
    sum_of_ages = 0
    count = friends['response']['count']
    for i in range(count):
        try:
            birthday_date_str = friends['response']['items'][i]['bdate']
            d, m, y = birthday_date_str.split('.')
            # all ok, there is birthday date, we can calculate age of
            # this friends
            date_today = datetime.date.today()
            birthday_date = datetime.date(int(y), int(m), int(d))
            delta_dates = date_today - birthday_date
            age = delta_dates.days // 365
            sum_of_ages += age
            count_real_friends += 1
        except:
            pass
    return sum_of_ages // count_real_friends
