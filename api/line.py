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
from api import logger
from errors.HTTPcode import STPHTTPException

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
            "code": 406
        }
        message = json.dumps(message)
        return message, 406

    token = flask.request.headers.get("token", None)
    if (token not in flask.session) or (flask.session[token] != "admin"):
        message = {"error": "limited authority", "code": 401}
        message = json.dumps(message)
        logger.warn("add subway line WARNING: limited authority.")
        logger.debug("POST /line/v1/add - 401")
        return message, 401

    name = data.get("name", None)
    logger.info("Begin to add subway line %s." % name)

    if name is None:
        message = {
            "error": "BadRequest: Invalid subway name.",
            "code": 400
        }
        message = json.dumps(message)
        logger.error("add subway line ERROR: BadRequest: Invalid subway name.")
        logger.debug("POST /line/v1/add - 400")
        return message, 400

    try:
        conductor.line.add_subway_line(name)
    except STPHTTPException as e:
        message = {
            "error": e.error_message,
            "code": e.httpcode
        }
        message = json.dumps(message)
        logger.error("add subway line ERROR:\n%s" % traceback.format_exc())
        logger.debug("POST /line/v1/add - %s" % e.httpcode)
        return message, e.httpcode

    message = {
        "success": "add subway line %s success." % name,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200