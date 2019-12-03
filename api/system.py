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
import conductor
import traceback
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
    token = flask.request.headers.get("token", None)
    if token not in flask.session:
        message = {
            "version": None,
            "error": "limited authority",
            "code": 401
        }
        message = json.dumps(message)
        logger.debug("GET /system/v1/version - 401")
        return message, 401

    try:
        version = (conductor.system.get_version()).strip()
    except STPHTTPException as e:
        message = {"version": None, "error": e.error_message, "code": e.httpcode}
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
    except json.decoder.JSONDecodeError:
        logger.error("login ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /system/v1/login - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    username = data.get("username", None)
    password = data.get("password", None)
    logger.info("user %s login..." % username)
    if (username is None) or (password is None):
        message = {
            "login": False,
            "token": None,
            "error": "BadRequest: Invalid username or password.",
            "code": 400
        }
        message = json.dumps(message)
        logger.error("user %s login ERROR: Invalid username or password."
                     % username)
        logger.debug("POST /system/v1/login - 400")
        return message, 400

    try:
        token = conductor.system.verify_user(username, password)
        for history_token in flask.session:
            if flask.session[history_token] == username:
                raise STPHTTPException("User logged in.", 403)
    except STPHTTPException as e:
        message = {
            "login": False,
            "token": None,
            "error": e.error_message,
            "code": e.httpcode
        }
        message = json.dumps(message)
        logger.error("user %s login ERROR: %s." % (username, e.error_message))
        logger.debug("POST /system/v1/login - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "login": True,
        "token": token,
        "code": 200
    }
    message = json.dumps(message)
    flask.session.permanent = True
    flask.session[token] = username
    conductor.system.update_token(username)
    logger.info("user %s login success." % username)
    logger.debug("POST /system/v1/login - 200")
    return message, 200


@system_blue.route("/logout", methods=["GET"])
def logout():
    username = flask.request.args.get("username", None)
    logger.info("user %s logout..." % username)
    if username is None:
        message = {
            "logout": False,
            "error": "BadRequest: Invalid username."
        }
        message = json.dumps(message)
        logger.error("Invalid user logout.")
        logger.debug("GET /system/v1/logout - 400")
        return message, 400

    token = flask.request.headers.get("token", None)
    if token not in flask.session:
        message = {"logout": False, "error": "limited authority"}
        message = json.dumps(message)
        logger.warn("Can not logout user %s: limited authority!" % username)
        logger.debug("GET /system/v1/logout - 401")
        return message, 401

    flask.session.pop(token)
    message = {"logout": True}
    message = json.dumps(message)
    logger.info("user %s logout success." % username)
    logger.debug("GET /system/v1/logout - 200")
    return message, 200


@system_blue.route("/session", methods=["GET"])
def get_session():
    token = flask.request.headers.get("token", None)
    if (token not in flask.session) or (flask.session[token] != "admin"):
        message = {"error": "limited authority"}
        message = json.dumps(message)
        logger.warn("Can not get session: limited authority!")
        logger.debug("GET /system/v1/session - 401")
        return message, 401

    message = {"session": dict(flask.session)}
    logger.debug("GET /system/v1/session - 200")
    logger.info("Get session: %s" % flask.session)
    return message, 200


@system_blue.route("/process", methods=["POST"])
def show_process():
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("get process list ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /system/v1/process - 406")
        message = {"error": "invalid POST request: JSON decode failed."}
        message = json.dumps(message)
        return message, 406

    admin_password = data.get("password", None)

    token = flask.request.headers.get("token", None)
    if (token not in flask.session) or (flask.session[token] != "admin"):
        message = {"error": "server shutdown failed"}
        message = json.dumps(message)
        logger.warn("try to get process list failed.")
        logger.debug("GET /system/v1/process - 401")
        return message, 401

    try:
        conductor.system.verify_user("admin", admin_password)
        pro_list = conductor.process_stack.show()
    except STPHTTPException as e:
        message = {"error": e.error_message}
        message = json.dumps(message)
        logger.debug("GET /system/v1/shutdown - %s" % e.httpcode)
        logger.warn("try to get process list failed.")
        return message, e.httpcode

    message = {"process": pro_list}
    message = json.dumps(message)
    logger.debug("GET /system/v1/process - 200")
    logger.warn("get process list.")
    return message, 200