"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/11
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database driver engine.
"""

import util
import configparser
import mysql.connector

def get_engine(database_name="subway"):
    root_path = util.get_root_path()
    url = root_path + "/conf/database.conf"
    conf = configparser.ConfigParser()
    conf.read(url)
    username = conf.get("database", "username")
    password = conf.get("database", "password")

    engine = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database=database_name,
        auth_plugin='mysql_native_password'
    )

    cursor = engine.cursor()
    return engine, cursor


def base_engine():
    root_path = util.get_root_path()
    url = root_path + "/conf/database.conf"
    conf = configparser.ConfigParser()
    conf.read(url)
    username = conf.get("database", "username")
    password = conf.get("database", "password")

    engine = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        auth_plugin='mysql_native_password'
    )

    cursor = engine.cursor()
    return engine, cursor