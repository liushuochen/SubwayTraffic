"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system log init
"""

import os
import util

def init():
    log_path = util.get_log_path()

    api_log_path = log_path + "/api"
    conductor_log_path = log_path + "/conductor"
    database_log_path = log_path + "/database"

    sub_log_path = [
        api_log_path,
        conductor_log_path,
        database_log_path
    ]

    for dir in sub_log_path:
        try:
            os.makedirs(dir)
        except FileExistsError:
            continue

    return