from datetime import date, timedelta


def get_date_list(start: date, end: date):
    # generates all dates between start date and end date
    # in required format

    date_list = []
    delta = end - start
    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        date_list.append(day)

    return date_list
