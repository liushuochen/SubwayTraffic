import datetime

if __name__ == '__main__':
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    print(now, type(now))