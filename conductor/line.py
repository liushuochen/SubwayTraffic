"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/01
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor for line.
"""

import util
import db.line
import compute.line
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
        raise STPHTTPException("subway line %s has been exist." %
                               subway_line_name,
                               403,
                               10200)

    uuid = util.generate_uuid(uuid_type="upper")
    db.line.add_subway_line(uuid, subway_line_name)

    new_line = compute.line.Line(uuid=uuid, name=subway_line_name)
    compute.line.lines[subway_line_name] = new_line
    return


def delete_subway_line(uuid):
    if not line_exist(uuid, "uuid"):
        raise STPHTTPException("subway %s has not exist." % uuid, 404, 10201)
    db.line.drop_subway_line(uuid)
    compute.line.delete_line(uuid)
    return


def update_line(**kwargs):
    uuid = kwargs["uuid"]
    name = kwargs["name"]

    if not line_exist(uuid, "uuid"):
        raise STPHTTPException("subway %s has not exist." % uuid, 404, 10201)
    if line_exist(name, "name"):
        raise STPHTTPException("subway name %s has already exist." % name,
                               403,
                               10202)

    db.line.update_subway_line(uuid, name)
    return


def get_all_line():
    return compute.line.line_list()


def details(uuid):
    lines = get_all_line()
    for line in lines:
        if line["uuid"] == uuid:
            target = line
            break
    else:
        raise STPHTTPException("can not find subway line %s" % uuid, 404)

    return target
