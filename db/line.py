"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/01
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver.
"""

import db.engine
from db import logger


def init_line():
    engine, cursor = db.engine.get_engine()
    sql = """
        create table if not exists subway_line(
        uuid  char(27) not null,
        name  varchar(10) not null,
        primary key(name)
        ) charset utf8
        """
    cursor.execute(sql)
    engine.close()
    logger.info("setup subway line finished.")
    return


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


def drop_subway_line(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "delete from subway_line where uuid=\"%s\"" % uuid
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def update_subway_line(uuid, name):
    engine, cursor = db.engine.get_engine()
    sql = "update subway_line set name=\"%s\" where uuid=\"%s\"" % \
          (name, uuid)
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def line_list():
    lines = []
    engine, cursor = db.engine.get_engine()
    sql = "select * from subway_line"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    for temp_data in db_data:
        pre_data = {}
        pre_data["uuid"] = temp_data[0]
        pre_data["name"] = temp_data[1]
        lines.append(pre_data)
    return lines


def line_exist(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "select count(1) from subway_line where uuid='%s'" % uuid
    cursor.execute(sql)
    data = cursor.fetchone()
    engine.close()
    return data[0]
