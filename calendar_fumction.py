import calendar

weekdays = {
    0: 'Понеделник',
    1: 'Вторник',
    2: 'Сряда',
    3: 'Четвъртък',
    4: 'Петък',
    5: 'Събота',
    6: 'Неделя',
}

def days(year, month):

    cal = calendar.Calendar()
    weekdays_in_month = [(x.day, weekdays[x.weekday()]) for x in cal.itermonthdates(year, month) if x.month == month]

    return weekdays_in_month





if __name__ == '__main__':
    print(days(2018, 1))