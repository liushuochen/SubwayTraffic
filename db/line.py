"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/01
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver.
"""

import db.engine


def subway_list():
    engine, cursor = db.engine.get_engine()
    sql = "select * from subway_line"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = []
    for pre_db_data in db_data:
        pre_data = {}
        pre_data["uuid"] = pre_db_data[0]
        pre_data["name"] = pre_db_data[1]
        data.append(pre_data)
    engine.close()
    return data


def add_subway_line(uuid, name):
    engine, cursor = db.engine.get_engine()
    sql = "insert into subway_line(uuid, name) values(%s, %s)"
    val = (uuid, name)
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return