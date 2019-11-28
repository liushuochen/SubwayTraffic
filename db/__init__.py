"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/19
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database init
"""

import configparser
import util
import conductor.system
import db.engine
from logs.logger import LOG

log_path = util.get_log_path()
logger = LOG(
    model="a",
    path=log_path,
    name="database"
)

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
    deploy_type = deploy_conf.get("deploy", "build_type")
    tables = get_all_tables(db_name)
    if "user" not in tables:
        create_user_table(deploy_conf)
    else:
        if deploy_type == "hard":
            pass

    return


def create_user_table(config):
    engine, cursor = db.engine.get_engine()
    sql = """
    create table user(
    username    varchar(23) not null,
    password    varchar(18) not null,
    token       char(10) not null,
    create_time datetime not null
    ) charset utf8
    """
    cursor.execute(sql)

    # add admin user
    admin_user = config.get("deploy", "admin_user")
    admin_pwd = config.get("deploy", "admin_pwd")
    now = util.get_time_string_format()
    token = conductor.system.general_token()
    sql = "insert into user(username, password, create_time, token) " \
          "values(%s, %s, %s, %s)"
    val = (admin_user, admin_pwd, now, token)
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