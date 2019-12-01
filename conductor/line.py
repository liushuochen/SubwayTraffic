"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/01
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor for line.
"""

import util
import db.line
from errors.HTTPcode import STPHTTPException

def add_subway_line(subway_line_name):
    if line_exit(subway_line_name):
        raise STPHTTPException("subway line %s has been exit." % subway_line_name,
                               403)

    uuid = util.generate_uuid(uuid_type="upper")
    db.line.add_subway_line(uuid, subway_line_name)
    return


def line_exit(name):
    lines = db.line.subway_list()
    for line in lines:
        if line["name"] == name:
            return True
    return False