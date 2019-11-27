"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system log init
"""

import os
import util
import time
from multiprocessing import Process
from conductor import process

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

    pro = Process(target=auto_clear_log)
    pro.start()

    return


def auto_clear_log():
    process.push(os.getpid())
    sleep_time = 12 * 3600
    while True:
        clear_logs()
        time.sleep(sleep_time)


def clear_logs():
    # TODO: get log create time. delete stale dated logs.
    pass