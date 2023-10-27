from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time

shared_lst_dates = []
list_markup = ()
old_month = -1

def create_calendar_markup(new_month):
    global old_month, list_markup, shared_lst_dates

    if old_month == new_month: #Speed up the markup making
        return list_markup

    today = datetime.date.today()
    year = today.year
    month = today.month
    dates = []
    shared_lst_dates = []
    old_month = new_month

    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    for day in range(1, last_day.day + 1):
        date = datetime.date(year, month, day)
        dates.append(InlineKeyboardButton(str(day), callback_data=date.strftime("%Y-%m-%d")))
        shared_lst_dates.append(date.strftime("%Y-%m-%d"))

    list_markup = InlineKeyboardMarkup([dates[i:i + 7] for i in range(0, len(dates), 7)])
    return list_markup

def get_shared_lst() -> tuple:
    return shared_lst_dates   