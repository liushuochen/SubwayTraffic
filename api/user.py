"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system api for user.
"""

import flask
import json
import conductor.user

user_blue = flask.Blueprint("user_blue",
                            __name__,
                            url_prefix='/user/v1')

@ user_blue.route("/users", methods=["GET"])
def user_list():
    token = flask.request.headers.get("token", None)
    if token not in flask.session:
        message = {"users": [], "error": "limited authority"}
        message = json.dumps(message)
        return message, 401

    users = conductor.user.users()
    message = {"users": users}
    message = json.dumps(message)
    return message, 200