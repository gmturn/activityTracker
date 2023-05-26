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


def convert_date_format(date_str):
    # convert the string to a datetime object
    date_obj = datetime.datetime.strptime(date_str, "%m/%d/%y")

    # format the date object back to a string in the desired format
    new_date_str = date_obj.strftime("%m/%d/%Y")

    return new_date_str
