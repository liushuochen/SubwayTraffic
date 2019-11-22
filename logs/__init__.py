"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system database init
"""

import os
import configparser
import util

def init():
    conf = configparser.ConfigParser()
    config_path = util.get_root_path() + "/conf/platform.conf"
    conf.read(config_path)
    log_path = conf.get("logs", "log_path")

    # init api log path
    api_log_path = log_path + "/api"
    conductor_log_path = log_path + "/conductor"

    try:
        os.makedirs(api_log_path)
        os.makedirs(conductor_log_path)
    except FileExistsError:
        return

    return