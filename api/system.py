"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system api for system
                    operation.
"""

import flask
import json
import conductor.system
from errors.HTTPcode import STPHTTPException

system_blue = flask.Blueprint("system_blue",
                              __name__,
                              url_prefix='/system/v1')

@ system_blue.route("/version", methods=["GET"])
def get_version():
    token = flask.request.headers.get("token", None)
    if token not in flask.session:
        message = {"version": None, "error": "limited authority"}
        message = json.dumps(message)
        return message, 401

    try:
        version = (conductor.system.get_version()).strip()
    except STPHTTPException as e:
        message = {"version": "None", "error": e.error_message}
        message = json.dumps(message)
        return message, e.httpcode

    message = {"version": version}
    message = json.dumps(message)
    return message, 200


@ system_blue.route("/login", methods=["POST"])
def login():
    data = json.loads(flask.request.data)
    username = data.get("username", None)
    password = data.get("password", None)
    if (username is None) or (password is None):
        message = {
            "login": False,
            "token": None,
            "error": "BadRequest: Invalid username or password."
        }
        message = json.dumps(message)
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
            "error": e.error_message
        }
        message = json.dumps(message)
        return message, e.httpcode

    message = {
        "login": True,
        "token": token,
    }
    message = json.dumps(message)
    flask.session.permanent = True
    flask.session[token] = username
    conductor.system.update_token("admin")
    return message, 200


@ system_blue.route("/logout", methods=["GET"])
def logout():
    username = flask.request.args.get("username", None)
    if username is None:
        message = {
            "logout": False,
            "error": "BadRequest: Invalid username."
        }
        message = json.dumps(message)
        return message, 400

    token = flask.request.headers.get("token", None)
    if token not in flask.session:
        message = {"logout": False, "error": "limited authority"}
        message = json.dumps(message)
        return message, 401

    flask.session.pop(token)
    message = {"logout": True}
    message = json.dumps(message)
    return message, 200


@ system_blue.route("/session", methods=["GET"])
def get_session():
    token = flask.request.headers.get("token", None)
    if (token not in flask.session) or (flask.session[token] != "admin"):
        message = {"error": "limited authority"}
        message = json.dumps(message)
        return message, 401

    message = {"session": dict(flask.session)}
    return message, 200