"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/01
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system subway line operate api
"""

import flask
import json
import traceback
import conductor.line
import conductor.user
import util
from api import logger
from errors.HTTPcode import STPHTTPException
from utils.httputils import http_code

line_blue = flask.Blueprint("line_blue", __name__, url_prefix="/line/v1")


@line_blue.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@line_blue.route("/add", methods=["POST"])
def add_line():
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("add subway line ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /line/v1/add - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": http_code.NotAcceptable,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, http_code.NotAcceptable

    token = flask.request.headers.get("token", None)
    if (token not in util.session) or \
            (not conductor.user.is_admin_user(util.session[token])):
        message = {
            "error": "limited authority",
            "code": http_code.Unauthorized,
            "tips": util.get_tips_dict(10006)
        }
        message = json.dumps(message)
        logger.warn("add subway line WARNING: limited authority.")
        logger.debug("POST /line/v1/add - 401")
        return message, http_code.Unauthorized

    name = data.get("name", None)
    try:
        logger.info("Begin to add subway line %s." % name)
        util.check_param(name=name)
        conductor.line.add_subway_line(name)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.error("add subway line %s ERROR:\n%s"
                     % (name, traceback.format_exc()))
        logger.debug("POST /line/v1/add - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "success": "add subway line %s success." % name,
        "code": http_code.OK
    }
    message = json.dumps(message)
    return message, http_code.OK


@line_blue.route("/delete", methods=["DELETE"])
def delete():
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("delete subway line ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("DELETE /line/v1/delete - %s" % http_code.NotAcceptable)
        message = {
            "error": "invalid DELETE request: JSON decode failed.",
            "code": http_code.NotAcceptable,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, http_code.NotAcceptable

    token = flask.request.headers.get("token", None)
    if (token not in util.session) or \
            (not conductor.user.is_admin_user(util.session[token])):
        message = {
            "error": "limited authority",
            "code": http_code.Unauthorized,
            "tips": util.get_tips_dict(10006)
        }
        message = json.dumps(message)
        logger.warn("delete subway line WARNING: limited authority.")
        logger.debug("DELETE /line/v1/delete - %s" % http_code.Unauthorized)
        return message, http_code.Unauthorized

    uuid = data.get("uuid", None)
    logger.info("Begin to delete subway line %s." % uuid)
    try:
        kwargs = {"uuid": uuid}
        util.check_param(**kwargs)
        conductor.line.delete_subway_line(uuid)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.error("delete subway line %s ERROR:\n%s"
                     % (uuid, traceback.format_exc()))
        logger.debug("DELETE /line/v1/delete - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "success": "delete subway line %s success." % uuid,
        "code": http_code.OK
    }
    message = json.dumps(message)
    return message, http_code.OK


@line_blue.route("/modify/<context>", methods=["PUT"])
def update_line(context):
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("modify subway line ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("PUT /line/v1/modify/%s - 406" % context)
        message = {
            "error": "invalid PUT request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    token = flask.request.headers.get("token", None)
    if (token not in util.session) or \
            (not conductor.user.is_admin_user(util.session[token])):
        message = {
            "error": "limited authority",
            "code": 401,
            "tips": util.get_tips_dict(10006)
        }
        message = json.dumps(message)
        logger.warn("update subway line WARNING: limited authority.")
        logger.debug("PUT /line/v1/modify/%s - 401" % context)
        return message, 401

    if context == "name":
        uuid = data.get("uuid", None)
        new_name = data.get("name", None)
        try:
            param = {
                "uuid": uuid,
                "name": new_name
            }
            util.check_param(**param)
            conductor.line.update_line(**param)
        except STPHTTPException as e:
            message = {
                "error": e.error_message,
                "code": e.httpcode,
                "tips": e.tip
            }
            message = json.dumps(message)
            logger.error("update subway line %s name ERROR:\n%s"
                         % (uuid, traceback.format_exc()))
            logger.debug("PUT /line/v1/modify/name - %s" % e.httpcode)
            return message, e.httpcode

        message = {
            "success": "update subway line %s success." % uuid,
            "code": 200
        }
        message = json.dumps(message)
        return message, 200
    else:
        message = {
            "error": "unknown modify request - '%s'" % context,
            "code": 404,
            "tips": util.get_tips_dict(10007)
        }
        message = json.dumps(message)
        return message, 404


@line_blue.route("/list", methods=["GET"])
def line_list():
    lines = conductor.line.get_all_line()
    message = {"line": lines, "code": 200}
    message = json.dumps(message)
    logger.debug("GET /line/v1/list - 200")
    return message, 200


@line_blue.route("/detail/<uuid>", methods=["GET"])
def line_detail(uuid):
    try:
        detail = conductor.line.details(uuid)
    except STPHTTPException as e:
        message = {
            "line": None,
            "error": e.error_message,
            "code": e.httpcode
        }
        message = json.dumps(message)
        logger.debug("GET /line/v1/detail/%s - %s" % (uuid, e.httpcode))
        logger.error("Get subway line %s detail ERROR: %s." % (uuid, e.error_message))
        return message, e.httpcode

    message = {
        "line": detail,
        "code": 200
    }
    message = json.dumps(message)
    logger.debug("GET /line/v1/detail/%s - 200" % uuid)
    return message, 200
