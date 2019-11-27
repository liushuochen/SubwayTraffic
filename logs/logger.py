"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system logger
"""

import os
import datetime


class LOG():
    def __init__(self, **kwargs):
        self.log_model = kwargs["model"]
        self.log_path = kwargs["path"]
        self.log_name = kwargs["name"]

    def info(self, message):
        file_name = generate_file_name("info")
        info_log_path = self.log_path + "/" + self.log_name + "/" + file_name
        write_logs(info_log_path, message, "a")

    def error(self, message):
        file_name = generate_file_name("error")
        error_log_path = self.log_path + "/" + self.log_name + "/" + file_name
        write_logs(error_log_path, message, "a")

    def warn(self, message):
        file_name = generate_file_name("warn")
        warn_log_path = self.log_path + "/" + self.log_name + "/" + file_name
        write_logs(warn_log_path, message, "a")

    def debug(self, message):
        file_name = generate_file_name("debug")
        debug_log_path = self.log_path + "/" + self.log_name + "/" + file_name
        write_logs(debug_log_path, message, "a")


def generate_file_name(level):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = date_str + level + ".log"
    return file_name


def write_logs(file, message, model):
    now = datetime.datetime.today().isoformat()[:-3]
    message = now + " " + message + "\n"
    if not os.path.exists(file):
        open(file, "w").write(message)
    else:
        open(file, model).write(message)