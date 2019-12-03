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

def line_exist(param, model):
    lines = db.line.subway_list()
    models = {"name", "uuid"}
    if model not in models:
        raise TypeError("Invalid model type %s." % model)

    for line in lines:
        if line[model] == param:
            return True
    return False


def add_subway_line(subway_line_name):
    if line_exist(subway_line_name, "name"):
        raise STPHTTPException("subway line %s has been exist." % subway_line_name,
                               403)

    uuid = util.generate_uuid(uuid_type="upper")
    db.line.add_subway_line(uuid, subway_line_name)
    return



def delete_subway_line(uuid):
    if not line_exist(uuid, "uuid"):
        raise STPHTTPException("subway %s has not exist." % uuid, 404)
    db.line.drop_subway_line(uuid)
    return