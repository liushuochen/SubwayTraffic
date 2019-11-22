"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system api init
"""

import configparser
import util
from logs.logger import LOG

conf_path = util.get_root_path() + "/conf/platform.conf"
conf = configparser.ConfigParser()
conf.read(conf_path)
log_path = conf.get("logs", "log_path")

logger = LOG(
    model="a",
    path=log_path,
    name="api"
)