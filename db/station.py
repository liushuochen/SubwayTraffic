"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2020/01/04
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver.
"""

import db.engine


def exist(name):
    engine, cursor = db.engine.get_engine()
    sql = "select count(1) from station where name='%s'" % name
    cursor.execute(sql)
    data = cursor.fetchone()
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
