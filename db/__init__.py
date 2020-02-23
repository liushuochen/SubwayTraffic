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
    import db.line
    from db.user import init_user
    from db.station import init_station
    from db.relation import init_relation
    from db.line import init_line
    from db.verify_code import init_verify_code
    platform_conf_path = util.get_root_path() + "/conf/platform.conf"
    database_conf_path = util.get_root_path() + "/conf/database.conf"
    deploy_conf = configparser.ConfigParser()
    deploy_conf.read([platform_conf_path, database_conf_path])

    # init database
    db_name = deploy_conf.get("deploy", "name")
    init_database(db_name)

    # init table
    init_user()
    init_line()
    init_verify_code()
    init_station()
    init_relation()
    lines = db.line.line_list()
    return lines


def init_database(name):
    logger.info("init database...")
    db_engine, cursor = db.engine.base_engine()
    sql = "create database if not exists %s charset utf8" % name
    cursor.execute(sql)
    db_engine.close()
    logger.info("setup database %s success." % name)
    return
