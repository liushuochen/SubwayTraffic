"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2020/01/04
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver.
"""

import db.engine


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