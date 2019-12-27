"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/19
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database init
"""

import configparser
import util
import db.engine
from logs.logger import LOG

log_path = util.get_log_path()
logger = LOG(
    model="a",
    path=log_path,
    name="database"
)

Admin = "admin"


def init():
    logger.info("init database...")
    platform_conf_path = util.get_root_path() + "/conf/platform.conf"
    database_conf_path = util.get_root_path() + "/conf/database.conf"
    deploy_conf = configparser.ConfigParser()
    deploy_conf.read([platform_conf_path, database_conf_path])

    # init database
    db_name = deploy_conf.get("deploy", "name")
    databases = get_all_database()
    if db_name not in databases:
        init_database(db_name)

    # init table
    tables = get_all_tables(db_name)
    if "user" not in tables:
        create_user_table(deploy_conf)

    if "subway_line" not in tables:
        create_subway_line_table()

    if "verify_code" not in tables:
        create_verify_code_table()

    if "station" not in tables:
        create_station_table()

    return


def create_verify_code_table():
    engine, cursor = db.engine.get_engine()
    sql = """
    create table verify_code(
    uuid    char(27),
    code    varchar(10) not null,
    operate varchar(20) not null,
    modify  datetime not null,
    primary key(uuid)
    ) charset utf8
    """
    cursor.execute(sql)
    engine.close()
    return


def create_subway_line_table():
    engine, cursor = db.engine.get_engine()
    sql = """
    create table subway_line(
    uuid  char(27) not null,
    name  varchar(10) not null,
    path  text not null,
    primary key(name)
    ) charset utf8
    """
    cursor.execute(sql)
    engine.close()
    return


def create_station_table():
    engine, cursor = db.engine.get_engine()
    sql = """
    create table station(
    uuid      char(27) not null,
    name      varchar(30),
    next_stop text,
    belong    tinytext,
    primary key(name)
    ) charset utf8
    """
    cursor.execute(sql)
    engine.close()
    return


def create_user_table(config):
    engine, cursor = db.engine.get_engine()
    sql = """
    create table user(
    uuid        char(27) not null,
    email       varchar(30),
    username    varchar(24) default "subway user",
    password    varchar(18) not null,
    token       char(10) not null,
    user_type   enum("admin", "user") not null default "user",
    create_time datetime not null,
    status      enum("active", "down", "lock") not null default "active",
    primary key(email)
    ) charset utf8
    """
    cursor.execute(sql)

    # add admin user
    uuid = util.generate_uuid()
    admin_user = config.get("deploy", "admin_user")
    admin_pwd = config.get("deploy", "admin_pwd")
    email = config.get("deploy", "admin_email")
    now = util.get_time_string_format()
    token = util.general_token()
    user_type = Admin
    sql = "insert into user " \
          "values(%s, %s, %s, %s, %s, %s, %s, default)"
    val = (uuid, email, admin_user, admin_pwd, token, user_type, now)
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return


def get_all_tables(db_name):
    engine, cursor = db.engine.get_engine(database_name=db_name)
    cursor.execute("show tables")
    db_data = cursor.fetchall()
    tables = []
    for table_tuple in db_data:
        tables.append(table_tuple[0])
    engine.close()
    return tables


def init_database(name):
    engine, cursor = db.engine.base_engine()
    sql = "create database %s charset utf8" % name
    cursor.execute(sql)
    engine.close()
    return


def get_all_database():
    engine, cursor = db.engine.base_engine()
    cursor.execute("show databases")
    db_data = cursor.fetchall()
    databases = []
    for database_tuple in db_data:
        databases.append(database_tuple[0])
    engine.close()
    return databases
