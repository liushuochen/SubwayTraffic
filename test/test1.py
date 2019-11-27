import datetime

if __name__ == '__main__':
    now_date = datetime.datetime.now().date()
    now_date_str = str(now_date)
    print(now_date, type(now_date))
    print(now_date_str, type(now_date_str))