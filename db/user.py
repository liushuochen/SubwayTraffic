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
from configparser import ConfigParser


def init_user():
    engine, cursor = db.engine.get_engine()
    sql = """
        create table if not exists user(
        uuid        char(27) not null,
        email       varchar(30),
        username    varchar(24) default "subway user",
        password    varchar(18) not null,
        token       char(10) not null,
        user_type   enum("admin", "user") not null default "user",
        create_time datetime not null,
        status      enum("active", "down", "lock") not null default "active",
        image       varchar(100),
        primary key(email)
        ) charset utf8
        """
    cursor.execute(sql)
    logger.info("Setup user finished.")

    # add admin user
    conf_path = util.get_root_path() + "/conf/platform.conf"
    deploy_conf = ConfigParser()
    deploy_conf.read([conf_path])
    uuid = util.generate_uuid()
    admin_user = deploy_conf.get("deploy", "admin_user")
    admin_pwd = deploy_conf.get("deploy", "admin_pwd")
    email = deploy_conf.get("deploy", "admin_email")
    image = "/root/image/localhost/default.jpeg"
    try:
        get_user_detail(email)
    except DBError:
        now = util.get_time_string_format()
        token = util.general_token()
        user_type = "admin"
        sql = "insert into user " \
              "values(%s, %s, %s, %s, %s, %s, %s, default, %s)"
        val = (uuid, email, admin_user, admin_pwd, token, user_type, now, image)
        cursor.execute(sql, val)
        logger.info("Init default admin user success.")
    engine.commit()
    engine.close()
    return


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
        pre_data["status"] = pre_db_data[7]
        data.append(pre_data)
    engine.close()
    return data


def get_user_detail(email):
    engine, cursor = db.engine.get_engine()
    sql = "select * from user where email='%s'" % email
    cursor.execute(sql)
    data = cursor.fetchall()
    if not data:
        logger.error("can not find user %s" % email)
        raise DBError("can not find user %s" % email, 404)
    user_details = data[0]
    engine.close()
    return user_details


def get_user_detail_by_uuid(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "select * from user where uuid='%s'" % uuid
    cursor.execute(sql)
    data = cursor.fetchall()
    if not data:
        logger.error("can not find user %s" % uuid)
        raise DBError("can not find user %s" % uuid, 404)
    detail = data[0]
    engine.close()
    return detail


# if username is a invalid username, update_token can not raise any errors
def update_token(email, token):
    engine, cursor = db.engine.get_engine()
    sql = "update user set token='%s' where email='%s'" % \
          (token, email)
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def update(**params):
    engine, cursor = db.engine.get_engine()
    sql = "update user set email='%s', username='%s', password='%s' " \
          "where uuid='%s'" % (params["email"],
                               params["username"],
                               params["password"],
                               params["uuid"]
                               )
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
    uuid = kwargs["uuid"]
    email = kwargs["email"]
    user_type = kwargs["user_type"]
    image = "/root/image/localhost/default.jpeg"
    sql = "insert into user values(%s, %s, %s, %s, %s, %s, %s, default, %s)"
    val = (uuid, email, username, password, token, user_type, create_time, image)
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return


def add_code(uuid, code, operate, modify_time):
    engine, cursor = db.engine.get_engine()
    sql = "insert into verify_code values(%s, %s, %s, %s)"
    val = (uuid, code, operate, modify_time)
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return


def drop_user(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "delete from user where uuid='%s'" % uuid
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def get_code_detail(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "select * from verify_code where uuid='%s'" % uuid
    cursor.execute(sql)
    data = cursor.fetchall()
    if not data:
        return data
    engine.close()
    return data[0]


def drop_code(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "delete from verify_code where uuid='%s'" % uuid
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def is_user_exist(email):
    engine, cursor = db.engine.get_engine()
    sql = "select count(1) from user where email='%s'" % email
    cursor.execute(sql)
    data = cursor.fetchone()
    engine.close()
    return data[0]


def lock(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "update user set status='lock' where uuid='%s'" % uuid
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def unlock(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "update user set status='active' where uuid='%s'" % uuid
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return


def update_photo(uuid, url):
    engine, cursor = db.engine.get_engine()
    sql = "update user set image='%s' where uuid='%s'" % \
          (url, uuid)
    cursor.execute(sql)
    engine.commit()
    engine.close()
    return
