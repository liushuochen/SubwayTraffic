"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/11
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver.
"""

import util
import db.engine
from errors.HTTPcode import DBError
from db import logger


def get_all_user_detail():
    engine, cursor = db.engine.get_engine()
    sql = "select * from user"
    cursor.execute(sql)
    db_data = cursor.fetchall()
    data = []
    for pre_db_data in db_data:
        pre_data = {}
        pre_data["uuid"] = pre_db_data[0]
        pre_data["email"] = pre_db_data[1]
        pre_data["username"] = pre_db_data[2]
        pre_data["password"] = pre_db_data[3]
        pre_data["token"] = pre_db_data[4]
        pre_data["type"] = pre_db_data[5]
        pre_data["create"] = \
            util.get_time_string_format(time_data=pre_db_data[6])
        data.append(pre_data)
    engine.close()
    return data


# if a invalid username, return a empty list `[]`
def get_user_detail(email):
    engine, cursor = db.engine.get_engine()
    sql = "select * from user where email=\"%s\"" % email
    cursor.execute(sql)
    data = cursor.fetchall()
    if not data:
        logger.error("can not find user %s" % email)
        raise DBError("can not find user %s" % email, 404)
    user_details = data[0]
    engine.close()
    return user_details


# if username is a invalid username, update_token can not raise any errors
def update_token(email, token):
    engine, cursor = db.engine.get_engine()
    sql =  "update user set token=\"%s\" where email=\"%s\"" % \
           (token, email)
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def update_pwd(username, password):
    engine, cursor = db.engine.get_engine()
    sql = "update user set password=\"%s\" where username=\"%s\"" % \
          (password, username)
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def add_user(**kwargs):
    engine, cursor = db.engine.get_engine()
    username = kwargs["username"]
    password = kwargs["password"]
    create_time = kwargs["register_time"]
    token = kwargs["token"]
    sql = "insert into user(username, password, create_time, token) " \
          "values(%s, %s, %s, %s)"
    val = (username, password, create_time, token)
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return


def drop_user(username):
    engine, cursor = db.engine.get_engine()
    sql = "delete from user where username=\"%s\"" % username
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return