"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system util tools.
"""

import os


def get_root_path():
    url_list = (os.path.abspath("")).split("/")
    url = ""
    for path in url_list:
        if path == "SubwayTraffic":
            url = url + path
            break
        url = url + path + "/"
    return url