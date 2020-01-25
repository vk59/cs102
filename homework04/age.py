import datetime
from statistics import median
from typing import Optional

from api import get_friends


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, fields='bdate')
    count_real_friends = 0
    sum_of_ages = 0
    count = friends['response']['count']
    for friend in friends:
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
