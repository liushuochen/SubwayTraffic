"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system api for user.
"""

import flask
import json
import traceback
import conductor.user
import util
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
    if token not in util.session or util.session[token] != "admin":
        message = {"users": [], "error": "limited authority", "code": 401}
        message = json.dumps(message)
        logger.debug("GET /user/v1/users - 401")
        logger.warn("Can not get user list info: limited authority.")
        return message, 401

    users = conductor.user.users()
    message = {"users": users, "code": 200}
    message = json.dumps(message)
    logger.debug("GET /user/v1/users - 200")
    return message, 200


@user_blue.route("/register", methods=["POST"])
def register_user():
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("register user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /user/v1/register - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    try:
        email = data.get("email", None)
        kwargs = {
            "username": data.get("username", None),
            "password": data.get("password", None),
            "email": email,
            "user_type": conductor.user.user
        }
        util.check_param(**kwargs)
        conductor.user.check_email(email)
        conductor.user.register(**kwargs)
    except STPHTTPException as e:
        message = {"error": e.error_message, "code": e.httpcode}
        message = json.dumps(message)
        logger.error("register user ERROR: %s\n%s." %
                     (e.error_message, traceback.format_exc()))
        logger.debug("POST /user/v1/register - %s" % e.httpcode)
        return message, e.httpcode

    message = {"success": "registered user %s success" % email, "code": 200}
    message = json.dumps(message)
    logger.info("register user %s success." % email)
    logger.debug("POST /user/v1/register - 200")
    return message, 200


@user_blue.route("/delete", methods=["DELETE"])
def delete_user():
    try:
        data = json.loads(flask.request.data)

        uuid = data.get("uuid", None)
        params = {"uuid": uuid}
        util.check_param(**params)

        token = flask.request.headers.get("token", None)
        if (token not in util.session) or \
                (not conductor.user.is_admin_user(util.session[token])):
            message = {"error": "limited authority", "code": 401}
            message = json.dumps(message)
            logger.debug("DELETE /user/v1/delete - 401")
            logger.warn("delete user WARNING: limited authority.")
            return message, 401

        conductor.user.destroy(uuid)

    except STPHTTPException as e:
        logger.error("delete user ERROR:\n %s" % traceback.format_exc())
        logger.debug("DELETE /user/v1/delete - %s" % e.httpcode)
        message = {"error": e.error_message, "code": e.httpcode}
        message = json.dumps(message)
        return message, e.httpcode

    except json.decoder.JSONDecodeError:
        logger.error("delete user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("DELETE /user/v1/delete - 406")
        message = {
            "error": "invalid DELETE request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    message = {"success": "delete user %s success" % uuid, "code": 200}
    message = json.dumps(message)
    logger.debug("DELETE /user/v1/delete - 200")
    logger.info("user %s has been deleted." % uuid)
    return message, 200


@user_blue.route("/modify/<context>", methods=["PUT"])
def update_user(context):
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        logger.error("modify user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("PUT /user/v1/modify/%s - 406" % context)
        message = {"error": "invalid PUT request: JSON decode failed."}
        message = json.dumps(message)
        return message, 406

    if context == "username":
        message = {"error": "can not change username."}
        message = json.dumps(message)
        logger.debug("PUT /user/v1/modify/username - 403")
        return message, 403

    elif context == "password":
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
        for sess in util.session:
            if util.session[sess] == username:
                util.session.pop(sess)
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
