import db.station


if __name__ == '__main__':
    data = db.station.get_list()
    print(data)
