"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/19
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database init
"""

import configparser
import util
import mysql.connector
import conductor.system
from logs.logger import LOG

log_path = util.get_log_path()
logger = LOG(
    model="a",
    path=log_path,
    name="database"
)

def init():
    print("Begin to init database...")

    platform_conf_path = util.get_root_path() + "/conf/platform.conf"
    database_conf_path = util.get_root_path() + "/conf/database.conf"
    deploy_conf = configparser.ConfigParser()
    deploy_conf.read([platform_conf_path, database_conf_path])

    # init database
    db_name = deploy_conf.get("deploy", "name")
    databases = get_all_database(deploy_conf)
    if db_name not in databases:
        init_database(db_name, deploy_conf)

    # init table
    deploy_type = deploy_conf.get("deploy", "build_type")
    tables = get_all_tables(deploy_conf)
    if "user" not in tables:
        create_user_table(deploy_conf)
    else:
        if deploy_type == "hard":
            pass

    print("init database finished.")
    return


def create_user_table(config):
    username = config.get("database", "username")
    password = config.get("database", "password")
    db_name = config.get("deploy", "name")

    mysql_db = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database=db_name,
        auth_plugin='mysql_native_password'
    )

    db_cursor = mysql_db.cursor()
    sql = """
    create table user(
    username    varchar(23),
    password    varchar(18),
    token       char(10),
    create_time datetime
    ) charset utf8
    """
    db_cursor.execute(sql)

    # add admin user
    admin_user = config.get("deploy", "admin_user")
    admin_pwd = config.get("deploy", "admin_pwd")
    now = util.get_time_string_format()
    token = conductor.system.general_token()
    sql = "insert into user(username, password, create_time, token) " \
          "values(%s, %s, %s, %s)"
    val = (admin_user, admin_pwd, now, token)
    db_cursor.execute(sql, val)
    mysql_db.commit()
    return


def get_all_tables(config):
    username = config.get("database", "username")
    password = config.get("database", "password")
    db_name = config.get("deploy", "name")

    mysql_db = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database=db_name,
        auth_plugin='mysql_native_password'
    )

    db_cursor = mysql_db.cursor()
    db_cursor.execute("show tables")
    db_data = db_cursor.fetchall()
    tables = []
    for table_tuple in db_data:
        tables.append(table_tuple[0])
    return tables


def init_database(name, config):
    username = config.get("database", "username")
    password = config.get("database", "password")

    mysql_db = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        auth_plugin='mysql_native_password'
    )

    db_cursor = mysql_db.cursor()
    sql = "create database %s charset utf8" % name
    db_cursor.execute(sql)
    return


def get_all_database(config):
    username = config.get("database", "username")
    password = config.get("database", "password")

    mysql_db = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        auth_plugin='mysql_native_password'
    )

    db_cursor = mysql_db.cursor()
    db_cursor.execute("show databases")
    db_data = db_cursor.fetchall()
    databases = []
    for database_tuple in db_data:
        databases.append(database_tuple[0])
    return databases