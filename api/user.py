"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system api for user.
"""

import flask
import json
import conductor.user
from errors.HTTPcode import STPHTTPException
from api import logger

user_blue = flask.Blueprint("user_blue",
                            __name__,
                            url_prefix='/user/v1')


@user_blue.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@user_blue.route("/users", methods=["GET"])
def user_list():
    token = flask.request.headers.get("token", None)
    if token not in flask.session or flask.session[token] != "admin":
        message = {"users": [], "error": "limited authority"}
        message = json.dumps(message)
        logger.debug("GET /user/v1/users - 401")
        logger.warn("Can not get user list info: limited authority.")
        return message, 401

    users = conductor.user.users()
    message = {"users": users}
    message = json.dumps(message)
    logger.debug("GET /user/v1/users - 200")
    return message, 200


@user_blue.route("/register", methods=["POST"])
def register_user():
    data = json.loads(flask.request.data)
    username = data.get("username", None)
    password = data.get("password", None)
    if username is None or password is None:
        message = {"error": "BadRequest: Invalid param"}
        message = json.dumps(message)
        logger.error("register user error: BadRequest: Invalid param.")
        logger.debug("POST /user/v1/register - 400")
        return message, 400

    try:
        conductor.user.register(username, password)
    except STPHTTPException as e:
        message = {"error": e.error_message}
        message = json.dumps(message)
        logger.error("register user error: %s." % e.error_message)
        logger.debug("POST /user/v1/register - %s" % e.httpcode)
        return message, e.httpcode

    message = {"success": "registered user %s success" % username}
    message = json.dumps(message)
    logger.info("register user %s success." % username)
    logger.debug("POST /user/v1/register - 200")
    return message, 200


@user_blue.route("/delete", methods=["DELETE"])
def delete_user():
    data = json.loads(flask.request.data)
    username = data.get("username", None)
    if username is None:
        message = {"error": "BadRequest: Invalid param"}
        message = json.dumps(message)
        logger.debug("DELETE /user/v1/delete - 400")
        return message, 400

    token = flask.request.headers.get("token", None)
    if (token not in flask.session) or (flask.session[token] != "admin"):
        message = {"error": "limited authority"}
        message = json.dumps(message)
        logger.debug("DELETE /user/v1/delete - 401")
        logger.warn("delete user WARNING: limited authority.")
        return message, 401

    try:
        conductor.user.destroy(username)
    except STPHTTPException as e:
        message = {"error": e.error_message}
        message = json.dumps(message)
        return message, e.httpcode

    message = {"success": "delete user %s success" % username}
    message = json.dumps(message)
    logger.debug("DELETE /user/v1/delete - 200")
    logger.info("user %s has been deleted." % username)
    return message, 200


@user_blue.route("/modify/<context>", methods=["PUT"])
def update_user(context):
    if context == "username":
        message = {"error": "can not change username."}
        message = json.dumps(message)
        logger.debug("PUT /user/v1/modify/username - 403")
        return message, 403

    elif context == "password":
        data = json.loads(flask.request.data)
        username = data.get("username", None)
        password = data.get("password", None)
        new_password = data.get("new_password", None)
        if (username is None) or (password is None) or (new_password is None):
            message = {"error": "BadRequest: Invalid param"}
            message = json.dumps(message)
            logger.debug("PUT /user/v1/modify/password - 400")
            logger.error("modify user %s password ERROR: BadRequest: Invalid "
                         "param." % username)
            return message, 400

        try:
            conductor.user.modify_user_pwd(username, password, new_password)
        except STPHTTPException as e:
            message = {"error": e.error_message}
            message = json.dumps(message)
            logger.debug("PUT /user/v1/modify/password - %s" % e.httpcode)
            return message, e.httpcode

        logger.info("change user %s password success, check user login..." %
                    username)
        for sess in flask.session:
            if flask.session[sess] == username:
                flask.session.pop(sess)
                logger.info("user %s logout after change password." % username)
                break

        message = {"success": "change password success."}
        message = json.dumps(message)
        logger.debug("PUT /user/v1/modify/password - 200")
        return message, 200
    else:
        message = {"error": "unknown modify request - '%s'" % context}
        message = json.dumps(message)
        return message, 404