"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system logger
"""

import os
import datetime


def write_logs(file, message, model):
    now = datetime.datetime.today().isoformat()[:-3]
    message = now + " " + message + "\n"
    if not os.path.exists(file):
        open(file, "w").write(message)
    else:
        open(file, model).write(message)


class LOG():
    def __init__(self, **kwargs):
        self.log_model = kwargs["model"]
        self.log_path = kwargs["path"]
        self.log_name = kwargs["name"]

    def info(self, message):
        info_log_path = self.log_path + "/" + self.log_name + "/info.log"
        write_logs(info_log_path, message, "a")

    def error(self, message):
        error_log_path = self.log_path + "/" + self.log_name + "/error.log"
        write_logs(error_log_path, message, "a")

    def warn(self, message):
        warn_log_path = self.log_path + "/" + self.log_name + "/warn.log"
        write_logs(warn_log_path, message, "a")

    def debug(self, message):
        debug_log_path = self.log_path + "/" + self.log_name + "/debug.log"
        write_logs(debug_log_path, message, "a")
