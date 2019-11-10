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
    try:
        version = (conductor.system.get_version()).strip()
    except STPHTTPException as e:
        message = {"version": "None", "error": e.error_message}
        return message, e.httpcode
    message = {"version": version}
    message = json.dumps(message)
    return message, 200