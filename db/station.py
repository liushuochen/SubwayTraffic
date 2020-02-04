"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2020/01/04
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver.

mysql> desc station;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| uuid      | char(27)    | NO   |     | NULL    |       |
| name      | varchar(30) | NO   | PRI | NULL    |       |
| next_stop | text        | YES  |     | NULL    |       |
+-----------+-------------+------+-----+---------+-------+

"""

import db.engine


def init_station():
    engine, cursor = db.engine.get_engine()
    sql = """
        create table if not exists station(
        uuid      char(27) not null,
        name      varchar(30),
        next_stop text,
        primary key(name)
        ) charset utf8
        """
    cursor.execute(sql)
    engine.close()
    return


def exist(value, types="name"):
    engine, cursor = db.engine.get_engine()
    sql = "select count(1) from station where %s='%s'" % (types, value)
    if types == "name":
        cursor.execute(sql)
        data = cursor.fetchone()
    elif types == "uuid":
        cursor.execute(sql)
        data = cursor.fetchone()
    else:
        raise TypeError("Unknown types %s." % types)
    engine.close()
    return data[0]


def add_station(**kwargs):
    engine, cursor = db.engine.get_engine()
    sql = "insert into station(uuid, name) values(%s, %s)"
    val = (kwargs["uuid"], kwargs["name"])
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return


def detail(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "select * from station where uuid='%s'" % uuid
    cursor.execute(sql)
    data = cursor.fetchall()[0]
    station_detail = {
        "uuid": data[0],
        "name": data[1],
        "next_stop": data[2],
        "belong": data[3]
    }
    return station_detail


def delete(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "delete from station where uuid='%s'" % uuid
    cursor.execute(sql)
    return


def update(uuid, name):
    engine, cursor = db.engine.get_engine()
    sql = "update station set name='%s' where uuid='%s'" % (name, uuid)
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def get_list():
    engine, cursor = db.engine.get_engine()
    sql = "select * from station"
    cursor.execute(sql)
    data = cursor.fetchall()
    station_list = []
    for station in data:
        each_detail = {}
        each_detail["uuid"] = station[0]
        each_detail["name"] = station[1]
        if station[3] is None:
            each_detail["belong"] = []
        else:
            each_detail["belong"] = station[3].split(",")
        station_list.append(each_detail)
    return station_list
