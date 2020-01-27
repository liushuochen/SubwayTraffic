"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/27
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system subway station operate api
"""

import flask
import json
import traceback
import conductor.user
import conductor.station
from api import logger
from errors.HTTPcode import *

station_blue = flask.Blueprint("station_blue", __name__, url_prefix="/station/v1")


@station_blue.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@station_blue.route("/add", methods=["POST"])
def add_station():
    try:
        data = json.loads(flask.request.data)
        token = flask.request.headers.get("token", None)
        if (token not in util.session) or \
                (not conductor.user.is_admin_user(util.session[token])):
            message = {
                "error": "limited authority",
                "code": 401,
                "tips": util.get_tips_dict(10006)
            }
            message = json.dumps(message)
            logger.warn("add subway station WARNING: limited authority.")
            logger.debug("POST /station/v1/add - 401")
            return message, 401
    except json.decoder.JSONDecodeError:
        logger.error("add subway station ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /station/v1/add - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    name = data.get("name", None)
    try:
        params = {
            "name": name,
        }
        util.check_param(**params)
        conductor.station.add_station(**params)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.error("add subway station %s ERROR:\n%s"
                     % (name, traceback.format_exc()))
        logger.debug("POST /station/v1/add - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "success": "add station %s success" % name,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200


@station_blue.route("/delete", methods=["DELETE"])
def delete_station():
    try:
        data = json.loads(flask.request.data)
        token = flask.request.headers.get("token", None)
        if (token not in util.session) or \
                (not conductor.user.is_admin_user(util.session[token])):
            message = {
                "error": "limited authority",
                "code": 401,
                "tips": util.get_tips_dict(10006)
            }
            message = json.dumps(message)
            logger.warn("delete subway station WARNING: limited authority.")
            logger.debug("DELETE /station/v1/delete - 401")
            return message, 401
    except json.decoder.JSONDecodeError:
        logger.error("delete subway station ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("DELETE /station/v1/delete - 406")
        message = {
            "error": "invalid DELETE request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    uuid = data.get("uuid", None)
    try:
        params = {"uuid": uuid}
        util.check_param(**params)
        conductor.station.delete(uuid)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.error("delete subway station %s ERROR:\n%s"
                     % (uuid, traceback.format_exc()))
        logger.debug("DELETE /station/v1/delete - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "success": "delete subway station %s success." % uuid,
        "code": 200
    }
    message = json.dumps(message)
    logger.debug("PUT /station/v1/update - 200")
    return message, 200


@station_blue.route("/update", methods=["PUT"])
def update_station():
    try:
        data = json.loads(flask.request.data)
        token = flask.request.headers.get("token", None)
        if (token not in util.session) or \
                (not conductor.user.is_admin_user(util.session[token])):
            message = {
                "error": "limited authority",
                "code": 401,
                "tips": util.get_tips_dict(10006)
            }
            message = json.dumps(message)
            logger.warn("update subway station WARNING: limited authority.")
            logger.debug("PUT /station/v1/update - 401")
            return message, 401
    except json.decoder.JSONDecodeError:
        logger.error("update subway station ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("PUT /station/v1/update - 406")
        message = {
            "error": "invalid PUT request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    uuid = data.get("uuid", None)
    new_name = data.get("name", None)
    try:
        params = {"uuid": uuid, "name": new_name}
        util.check_param(**params)
        conductor.station.update(uuid, new_name)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.error("update subway station %s ERROR:\n%s"
                     % (uuid, traceback.format_exc()))
        logger.debug("PUT /station/v1/update - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "success": "update subway station %s success." % uuid,
        "code": 200
    }
    message = json.dumps(message)
    logger.debug("PUT /station/v1/update - 200")
    return message, 200


@station_blue.route("/list", methods=["GET"])
def station_list():
    try:
        token = flask.request.headers.get("token", None)
        if (token not in util.session) or \
                (not conductor.user.is_admin_user(util.session[token])):
            raise STPHTTPException("limited authority", 401, 10001)
        stations = conductor.station.get_list()
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.debug("GET /station/v1/list - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "stations": stations,
        "code": 200
    }
    message = json.dumps(message)
    logger.debug("GET /station/v1/list - 200")
    return message, 200
