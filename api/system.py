"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system api for system
                    operation.
"""

import flask
import json
import conductor.system
import conductor.user
import conductor
import traceback
import util
from api import logger
from errors.HTTPcode import STPHTTPException

system_blue = flask.Blueprint("system_blue",
                              __name__,
                              url_prefix='/system/v1')


@system_blue.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@system_blue.route("/version", methods=["GET"])
def get_version():
    try:
        token = flask.request.headers.get("token", None)
        if token not in util.session:
            raise STPHTTPException("limited authority", 401, 10001)
        version = (conductor.system.get_version()).strip()
    except STPHTTPException as e:
        message = {
            "version": None,
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.debug("GET /system/v1/version - %s" % e.httpcode)
        return message, e.httpcode

    message = {"version": version, "code": 200}
    message = json.dumps(message)
    logger.debug("GET /system/v1/version - 200")
    return message, 200


@system_blue.route("/login", methods=["POST"])
def login():
    try:
        data = json.loads(flask.request.data)
        email = data.get("email", None)
        password = data.get("password", None)
        logger.info("user %s login..." % email)
    except json.decoder.JSONDecodeError:
        logger.error("login ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /system/v1/login - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    try:
        kwargs = {
            "email": email,
            "password": password
        }
        util.check_param(**kwargs)
        uuid, token, user_type = conductor.system.verify_user(email, password)
        for history_token in util.session:
            if util.session[history_token] == uuid:
                raise STPHTTPException("User logged in.", 403, 10100)
    except STPHTTPException as e:
        message = {
            "login": False,
            "token": None,
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        logger.error("user %s login ERROR: %s." % (email, e.error_message))
        logger.debug("POST /system/v1/login - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "login": True,
        "token": token,
        "type": user_type,
        "code": 200
    }
    message = json.dumps(message)
    util.session[token] = uuid
    conductor.system.update_token(email)
    logger.info("user %s login success." % email)
    logger.debug("POST /system/v1/login - 200")
    return message, 200


@system_blue.route("/logout", methods=["GET"])
def logout():
    token = flask.request.headers.get("token", None)
    if token not in util.session:
        message = {
            "logout": False,
            "error": "limited authority.",
            "code": 401,
            "tips": util.get_tips_dict(10001)
        }
        message = json.dumps(message)
        logger.warn("unknown user logout.")
        logger.debug("GET /system/v1/logout - 401")
        return message, 401

    uuid = util.session.pop(token)
    message = {"logout": True, "code": 200}
    message = json.dumps(message)
    logger.info("user %s logout success." % uuid)
    logger.debug("GET /system/v1/logout - 200")
    return message, 200


@system_blue.route("/session", methods=["GET"])
def get_session():
    token = flask.request.headers.get("token", None)
    if (token not in util.session) or \
            (not conductor.user.is_admin_user(util.session[token])):
        message = {
            "error": "limited authority",
            "code": 401,
            "tips": util.get_tips_dict(10006)
        }
        message = json.dumps(message)
        logger.warn("Can not get session: limited authority!")
        logger.debug("GET /system/v1/session - 401")
        return message, 401

    message = {"session": util.session, "code": 200}
    logger.debug("GET /system/v1/session - 200")
    logger.info("Get session: %s" % util.session)
    return message, 200


@system_blue.route("/process", methods=["POST"])
def show_process():
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("get process list ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /system/v1/process - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    admin_password = data.get("password", None)

    token = flask.request.headers.get("token", None)
    if (token not in util.session) or (util.session[token] != "admin"):
        message = {"error": "server shutdown failed", "code": 401}
        message = json.dumps(message)
        logger.warn("try to get process list failed.")
        logger.debug("GET /system/v1/process - 401")
        return message, 401

    try:
        conductor.system.verify_user("admin", admin_password)
        pro_list = conductor.process_stack.show()
    except STPHTTPException as e:
        message = {"error": e.error_message, "code": e.httpcode}
        message = json.dumps(message)
        logger.debug("GET /system/v1/shutdown - %s" % e.httpcode)
        logger.warn("try to get process list failed.")
        return message, e.httpcode

    message = {"process": pro_list, "code": 200}
    message = json.dumps(message)
    logger.debug("GET /system/v1/process - 200")
    logger.warn("get process list.")
    return message, 200


@system_blue.route("/live", methods=["GET", "POST"])
def is_running():
    now = util.get_time_string_format()
    message = {
        "detail": "SubwayTraffic service is running now %s" % now,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200
