import datetime


def getCurrentMonth():
    return datetime.datetime.now().month


def getCurrentDay():
    return datetime.datetime.now().day


def getCurrentYearYYYY():
    return datetime.datetime.now().year


def getCurrenYearYY():
    # Extract the last two digits of the year
    return datetime.datetime.now().year % 100
