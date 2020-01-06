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
from errors.HTTPcode import *
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
    if (token not in util.session) or \
            (not conductor.user.is_admin_user(util.session[token])):
        message = {
            "users": [],
            "error": "limited authority",
            "code": 401,
            "tips": util.get_tips_dict(10006)
        }
        message = json.dumps(message)
        logger.debug("GET /user/v1/users - 401")
        logger.warn("Can not get user list info: limited authority.")
        return message, 401

    users = conductor.user.users()
    message = {"users": users, "code": 200}
    message = json.dumps(message)
    logger.debug("GET /user/v1/users - 200")
    return message, 200


@user_blue.route("/exist", methods=["POST"])
def find_user():
    try:
        data = json.loads(flask.request.data)
        email = data.get("email", None)
        kwargs = {
            "email": email
        }
        util.check_param(**kwargs)
        conductor.user.check_email(email)
    except STPHTTPException as e:
        logger.debug("POST /user/v1/exist - %s" % e.httpcode)
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        return message, e.httpcode
    except json.decoder.JSONDecodeError:
        logger.error("exist user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /user/v1/exist - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    exit_detail = conductor.user.is_user_exist(email)
    message = exit_detail
    message["code"] = 200
    message = json.dumps(message)
    logger.debug("POST /user/v1/exist - 200")
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
            "code": 406,
            "tips": util.get_tips_dict(10004)

        }
        message = json.dumps(message)
        return message, 406

    try:
        email = data.get("email", None)
        kwargs = {
            "username": data.get("username", None),
            "password": data.get("password", None),
            "email": email,
            "user_type": conductor.user.normal_user
        }
        util.check_param(**kwargs)
        conductor.user.check_email(email)
        conductor.user.register(**kwargs)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
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
            message = {
                "error": "limited authority",
                "code": 401,
                "tips": util.get_tips_dict(10006)
            }
            message = json.dumps(message)
            logger.debug("DELETE /user/v1/delete - 401")
            logger.warn("delete user WARNING: limited authority.")
            return message, 401

        conductor.user.destroy(uuid)

    except STPHTTPException as e:
        logger.error("delete user ERROR:\n %s" % traceback.format_exc())
        logger.debug("DELETE /user/v1/delete - %s" % e.httpcode)
        message = {
            "error": e.error_message,
            "code": e.httpcode,
            "tips": e.tip
        }
        message = json.dumps(message)
        return message, e.httpcode

    except json.decoder.JSONDecodeError:
        logger.error("delete user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("DELETE /user/v1/delete - 406")
        message = {
            "error": "invalid DELETE request: JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    message = {"success": "delete user %s success" % uuid, "code": 200}
    message = json.dumps(message)
    logger.debug("DELETE /user/v1/delete - 200")
    logger.info("user %s has been deleted." % uuid)
    return message, 200


@user_blue.route("/modify", methods=["PUT"])
def update_user():
    try:
        data = json.loads(flask.request.data)
        uuid = data.get("uuid", None)
        email = data.get("email", None)

        kwargs = {
            "uuid": uuid,
            "email": email,
            "username": '',
            "verify_code": data.get("verify_code", None)
        }
        util.check_param(**kwargs)
        conductor.user.check_verify_code(**kwargs)

        if "new_email" in data:
            kwargs["new_email"] = data["new_email"]
        if "new_username" in data:
            kwargs["new_username"] = data["new_username"]
        if "new_password" in data:
            kwargs["new_password"] = data["new_password"]
        conductor.user.update(**kwargs)
    except json.decoder.JSONDecodeError:
        logger.error("modify user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("PUT /user/v1/modify - 406")
        message = {
            "error": "invalid PUT request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406
    except STPHTTPException as e:
        message = {"error": e.error_message, "code": e.httpcode}
        message = json.dumps(message)
        logger.debug("PUT /user/v1/modify - %s" % e.httpcode)
        logger.error("modify user ERROR:\n %s" % traceback.format_exc())
        return message, e.httpcode
    except DBError as e:
        message = {"error": e.error_message, "code": e.error_code}
        message = json.dumps(message)
        logger.debug("PUT /user/v1/modify - %s" % e.error_code)
        logger.error("modify user ERROR:\n %s" % traceback.format_exc())
        return message, e.error_code

    message = {
        "success": "update user %s success." % uuid,
        "code": 200
    }
    message = json.dumps(message)
    logger.info("update user %s success." % uuid)
    logger.debug("PUT /user/v1/modify - 200")
    return message, 200


@user_blue.route("/lock", methods=["POST"])
def lock():
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
            logger.debug("POST /user/v1/lock - 401")
            logger.warn("lock user %s WARNING: limited authority." % uuid)
            return message, 401

        conductor.user.lock(uuid)
    except DuplicateException as e:
        message = {
            "success": e.error_message,
            "code": e.httpcode
        }
        message = json.dumps(message)
        logger.info(e.error_message)
        logger.debug("POST /user/v1/lock - %s" % e.httpcode)
        return message, e.httpcode
    except STPHTTPException as e:
        message = {"error": e.error_message, "code": e.httpcode}
        message = json.dumps(message)
        logger.debug("POST /user/v1/lock - %s" % e.httpcode)
        logger.error("lock user ERROR:\n %s" % traceback.format_exc())
        return message, e.httpcode
    except json.decoder.JSONDecodeError as e:
        logger.error("lock user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /user/v1/lock - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    logger.info("user %s has been locked." % uuid)
    message = {
        "success": "user %s locked success" % uuid,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200


@user_blue.route("/unlock", methods=["POST"])
def unlock():
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
            logger.debug("POST /user/v1/unlock - 401")
            logger.warn("unlock user %s WARNING: limited authority." % uuid)
            return message, 401

        conductor.user.unlock(uuid)
    except DuplicateException as e:
        message = {
            "success": e.error_message,
            "code": e.httpcode
        }
        message = json.dumps(message)
        logger.info(e.error_message)
        logger.debug("POST /user/v1/unlock - %s" % e.httpcode)
        return message, e.httpcode
    except STPHTTPException as e:
        message = {"error": e.error_message, "code": e.httpcode}
        message = json.dumps(message)
        logger.debug("POST /user/v1/unlock - %s" % e.httpcode)
        logger.error("unlock user ERROR:\n %s" % traceback.format_exc())
        return message, e.httpcode
    except json.decoder.JSONDecodeError as e:
        logger.error("unlock user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /user/v1/unlock - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    logger.info("unlock user %s success." % uuid)
    message = {
        "success": "unlock user %s success." % uuid,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200


@user_blue.route("/live", methods=["POST"])
def is_live():
    try:
        data = json.loads(flask.request.data)
    except json.decoder.JSONDecodeError:
        message = {
            "error": "JSON decode failed.",
            "code": 406,
            "tips": util.get_tips_dict(10004)
        }
        message = json.dumps(message)
        return message, 406

    post_token = data.get("token", None)
    if post_token in util.session:
        is_login = True
    else:
        is_login = False

    message = {
        "is_login": is_login,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200
