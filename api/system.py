"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system api for system operation.
"""

import flask
import json
import conductor.system
from errors.HTTPcode import STPHTTPException

system_blue = flask.Blueprint("system_blue", __name__, url_prefix='/system/v1')

@ system_blue.route("/version", methods=["GET"])
def get_version():
    # token = flask.request.headers.get("Token")
    # if (token != "liushuochen") or (token is None):
    #     message = {"version": "None", "error": "limited authority"}
    #     message = json.dumps(message)
    #     return message, 401
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
    data = flask.request.data
    data = json.loads(data)
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
        if username in flask.session:
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
    flask.session[username] = token
    return message, 200