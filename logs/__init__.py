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
import datetime
import conductor
from multiprocessing import Process

def init():
    sub_log_path = sub_logs()
    for dir in sub_log_path:
        try:
            os.makedirs(dir)
        except FileExistsError:
            continue

    pro = Process(target=auto_clear_log, args=(conductor.process_queue,))
    pro.start()

    child_pid = conductor.process_queue.get()
    conductor.process_stack.push(child_pid)

    return


def auto_clear_log(queue):
    pid = os.getpid()
    queue.put(pid)

    # each 12 hours running once
    sleep_time = 12 * 3600
    while True:
        clear_logs()
        time.sleep(sleep_time)


def sub_logs():
    log_path = util.get_log_path()

    api_log_path = log_path + "/api"
    conductor_log_path = log_path + "/conductor"
    database_log_path = log_path + "/database"

    sub_log_path = [
        api_log_path,
        conductor_log_path,
        database_log_path
    ]
    return sub_log_path


def clear_logs():
    sub_log_path = sub_logs()
    for dir in sub_log_path:
        try:
            logs = log_filter(os.listdir(dir))
            check_logs(logs, dir)
        except FileNotFoundError:
            continue


def check_logs(log_list, dir):
    for log_file in log_list:
        atom = log_file.split("-")
        year = atom[0]
        month = atom[1]
        day = atom[2][:2]
        create_date = datetime.date(int(year), int(month), int(day))
        now_date = datetime.datetime.now().date()
        if (now_date - create_date).days > 3:
            path = dir + "/" + log_file
            os.remove(path)


def log_filter(log_list):
    logs = []
    for log_path in log_list:
        suffix = log_path.split(".")[-1]
        if suffix == "log":
            logs.append(log_path)
    return logs