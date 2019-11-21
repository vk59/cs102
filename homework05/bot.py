import requests
import json
import telebot
import time
import datetime
from datetime import date
from bs4 import BeautifulSoup
from typing import List, Tuple


days = {
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
    'sunday': 7
}


days_in_russian = {
    'monday': 'Понедельник',
    'tuesday': 'Вторник',
    'wednesday': 'Среда',
    'thursday': 'Четверг',
    'friday': 'Пятница',
    'saturday': 'Суббота',
    'sunday': 'Воскресенье'
}

with open('config.json') as con:
    config = json.load(con)


telebot.apihelper.proxy = {'https': 'https://117.1.16.131:8080'}
bot = telebot.TeleBot(config["access_token"])


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = f'{config["domain"]}/{group}/{week}raspisanie_zanyatiy_{group}.htm'
    print(url)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, num_of_day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на текущий день
    schedule_table = soup.find("table", attrs={"id": f"{num_of_day}day"})
    if schedule_table is None:
        return [],[],[],False
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list, True


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    mes = message.text.split()
    day = mes[0]
    num_week = ''
    if len(mes) == 2:
        group = mes[1]
    elif len(mes) == 3:
        num_week = mes[1]
        group = mes[2]
        print(num_week)
    print(group)
    web_page = get_page(group, num_week)
    times_lst, locations_lst, lessons_lst, is_there_lessons = \
        parse_schedule_for_a_day(web_page, days[day[1:]])
    resp = ''
    if is_there_lessons:
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode = 'HTML')
    else:
        bot.send_message(message.chat.id, '<b>В этот день нет занятий</b>', parse_mode = 'HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    mes = message.text.split()
    group = mes[1]
    # title of message
    resp = '<b> ВСЁ РАСПИСАНИЕ </b> \n'
    # going to check all the timetable (from the first weel to second)
    for week in range(1, 3):
        for day in days:
            this_day_num = days[day]
            if week == 1:
                week_str = 'чётная'
            elif week == 2:
                week_str = 'нечётная'
            # writing name of day (num and week)
            resp += f'<b>{days_in_russian[day]}</b>, неделя {week_str}'
            web_page = get_page(group, week)
            times_lst, locations_lst, lessons_lst, is_there_lessons = \
                parse_schedule_for_a_day(web_page, this_day_num)
            # check, are there lessons or not
            if is_there_lessons:
                for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
            else:
                resp += '<b> Нет занятий </b>\n'
    # send message
    bot.send_message(message.chat.id, resp, parse_mode = 'HTML')

    
if __name__ == '__main__':
    bot.polling(none_stop=True)

