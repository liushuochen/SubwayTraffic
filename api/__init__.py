"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/22
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system api init
"""

import util
from logs.logger import LOG

log_path = util.get_log_path()

logger = LOG(
    model="a",
    path=log_path,
    name="api"
)