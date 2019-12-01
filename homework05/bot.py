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
    'monday': 'ПОНЕДЕЛЬНИК',
    'tuesday': 'ВТОРНИК',
    'wednesday': 'СРЕДА',
    'thursday': 'ЧЕТВЕРГ',
    'friday': 'ПЯТНИЦА',
    'saturday': 'СУББОТА',
    'sunday': 'ВОСКРЕСЕНЬЕ'
}

CASHED_TIMETABLE = {}


with open('config.json') as con:
    config = json.load(con)

telebot.apihelper.proxy = {'https': 'https://54.37.131.235:3128'}
bot = telebot.TeleBot(config["access_token"])


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = f'{config["domain"]}/{group}/{week}raspisanie_zanyatiy_{group}.htm'
    # print(url)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_day(web_page, num_of_day):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на текущий день
    schedule_table = soup.find("table", attrs={"id": f"{num_of_day}day"})
    if schedule_table is None:
        return None
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join(
        [info for info in lesson_info if info])
        for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def get_schedule_cash(group, day, week=''):
    '''
    Examples of parameters:
        group = 'K3140'
        day = '1'
        week = '2'
    out:
        [[], [], []]
    or: None (if there is not lessons)
    '''
    if week == '':
        week_num = 0
    else:
        week_num = int(week)

    global CASHED_TIMETABLE
    global days
    if CASHED_TIMETABLE.get(group) is None:
        CASHED_TIMETABLE[group] = {}
    if CASHED_TIMETABLE[group].get(week_num) is None:
        CASHED_TIMETABLE[group][week_num] = {}
    if CASHED_TIMETABLE[group][week_num].get(day) is None:
        web_page = get_page(group, week)
        schedule = parse_schedule_for_a_day(web_page, day)
        if schedule is None:
            CASHED_TIMETABLE[group][week_num][day] = [
                [[], [], []], date.today()]
            return None
        else:
            CASHED_TIMETABLE[group][week_num][day] = [
                schedule, date.today()]
            return schedule
    # checking when the latest downloading of schedule was
    elif date.today() \
        - CASHED_TIMETABLE[group][week_num][day][1] > datetime.timedelta(
            days=7):
        web_page = get_page(group, week)
        schedule = parse_schedule_for_a_day(web_page, day)
        if schedule is None:
            CASHED_TIMETABLE[group][week_num][day] = [
                [[], [], []], date.today()]
        else:
            CASHED_TIMETABLE[group][week_num][day] = [
                schedule, date.today()]
    else:
        schedule = CASHED_TIMETABLE[group][week_num][day][0]
        if schedule[0] == []:
            return None
        else:
            return schedule


@bot.message_handler(commands=[
    'monday', 'tuesday', 'wednesday', 'thursday',
    'friday', 'saturday', 'sunday'])
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
    schedule = get_schedule_cash(group, days[day[1:]], num_week)
    resp = ''
    if schedule is not None:
        times_lst, locations_lst, lessons_lst = schedule
        for time, location, lession in zip(
                times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        bot.send_message(
            message.chat.id,
            '<b>В этот день нет занятий</b>',
            parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    date_first_week = datetime.date(2019, 11, 18)
    mes = message.text.split()
    group = mes[1]
    time_now = datetime.datetime.now()
    hour_now = time_now.hour
    minute_now = time_now.minute
    date_today = date.today()
    date_of_lesson = date.today()
    day_today = date_today.isoweekday()
    week_today = (date_today - date_first_week).days // 7 % 2 + 1
    bot.send_message(
        message.chat.id, 'Загружаем расписание...', parse_mode='HTML')
    schedule = get_schedule_cash(group, day_today, week_today)
    # explore near schedule
    # checking if there is not lessons today (and if they finished)
    Flag = False
    # checking if lessons finished
    if schedule is not None:
        times_lst, locations_lst, lessons_lst = schedule
        hour = int(times_lst[len(times_lst)-1][0:2])
        minute = int(times_lst[len(times_lst)-1][3:5])
        if hour > hour_now or (hour == hour_now and minute > minute_now):
            Flag = True
    while schedule is None or Flag:
        date_of_lesson = date_of_lesson + datetime.timedelta(days=1)
        day_of_lesson = date_of_lesson.isoweekday()
        week_today = (date_of_lesson - date_first_week).days // 7 % 2 + 1
        schedule = get_schedule_cash(group, day_of_lesson, week_today)
        if schedule is not None:
            times_lst, locations_lst, lessons_lst = schedule
            hour = int(times_lst[len(times_lst)-1][0:2])
            minute = int(times_lst[len(times_lst)-1][3:5])
            if hour < hour_now or hour == hour_now and minute < minute_now:
                Flag = True
            else:
                Flag = False
    times_lst, locations_lst, lessons_lst = schedule
    bot.send_message(
        message.chat.id, 'Ищем ближайшее занятие...', parse_mode='HTML')
    for i in range(len(times_lst)):
        hour = int(times_lst[i][0:2])
        minute = int(times_lst[i][3:5])
        if date_today < date_of_lesson:
            resp = f'Ближайшее занятие состоится {date_of_lesson}: \n'
            resp += '<b>{}</b>, {}, {}\n'.format(
                times_lst[0], locations_lst[0], lessons_lst[0])
            break
        elif hour_now < hour:
            resp = f'Ближайшее занятие состоится {date_of_lesson}: \n'
            resp += '<b>{}</b>, {}, {}\n'.format(
                times_lst[i], locations_lst[i], lessons_lst[i])
            break
        elif minute_now < minute:
            resp = f'Ближайшее занятие состоится {date_of_lesson}: \n'
            resp += '<b>{}</b>, {}, {}\n'.format(
                times_lst[i], locations_lst[i], lessons_lst[i])
            break
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # date from today
    mes = message.text.split()
    group = mes[1]
    date_first_week = datetime.date(2019, 11, 18)
    date_tomorrow = date.today() + datetime.timedelta(days=1)
    day_tomorrow = date_tomorrow.isoweekday()
    week_tomorrow = (date_tomorrow - date_first_week).days // 7 % 2 + 1
    resp = 'Ищем расписание на завтра...'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    schedule = get_schedule_cash(group, day_tomorrow, week_tomorrow)
    # поиск занятий на завтра (или на следующий рабочий день)
    while schedule is None:
        date_tomorrow = date_tomorrow + datetime.timedelta(days=1)
        day_tomorrow = date_tomorrow.isoweekday()
        week_tomorrow = (date_tomorrow - date_first_week).days // 7 % 2 + 1
        schedule = get_schedule_cash(group, day_tomorrow, week_tomorrow)
    d = date_tomorrow.day
    m = date_tomorrow.month
    y = date_tomorrow.year
    resp = f'Занятия на следующий рабочий день <b>{d}.{m}.{y}</b>:\n\n'
    times_lst, locations_lst, lessons_lst = schedule
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    mes = message.text.split()
    group = mes[1]
    # title of message
    resp = f'<b>ВСЁ РАСПИСАНИЕ гр. {group}</b>'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')
    # going to check all the timetable (from the first weel to second)
    for week in range(1, 3):
        resp = ''
        for day in days:
            this_day_num = days[day]
            if week == 1:
                week_str = 'чётная'
            elif week == 2:
                week_str = 'нечётная'
            # writing name of day (num and week)
            resp += f'<b>{days_in_russian[day]}</b>, неделя {week_str}\n\n'
            # getting timetable
            schedule = get_schedule_cash(group, this_day_num, str(week))
            # check, are there lessons or not
            if schedule is not None:
                times_lst, locations_lst, lessons_lst = schedule
                for time, location, lession in zip(
                        times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(
                            time, location, lession)
            else:
                resp += '<b>Нет занятий</b>\n'
        # send message
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
