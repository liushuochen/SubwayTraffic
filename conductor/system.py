"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system conductor for system
                    operation.
"""

import util

def get_version():
    root_path = util.get_root_path()
    url = root_path + "/conf/stp.version"
    version = open(url).read()
    return version