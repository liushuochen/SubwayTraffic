"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/25
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system process send email
                    operation.
"""

import flask
import json
import util
import conductor.user
import traceback
from errors.HTTPcode import STPHTTPException
from api import logger
from utils.httputils import http_code

email_blue = flask.Blueprint("email_blue", __name__, url_prefix="/email/v1")


@email_blue.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@email_blue.route("/code", methods=["POST"])
def send_code_email():
    try:
        data = json.loads(flask.request.data)

        params = {
            "receiver": data.get("receiver", None),
            "header": data.get("header", None),
            "operate": data.get("operate", None)
        }
        util.check_param(**params)
        verify_code = util.general_verify_code(6)
        kwargs = {
            "header": params["header"],
            "type": "send_code",
            "receiver": params["receiver"],
            "operate": params["operate"],
            "code": verify_code
        }
        from main import send_mail
        send_mail(**kwargs)

        conductor.user.push_verify_code(kwargs["receiver"],
                                        verify_code,
                                        kwargs["operate"])

        message = {
            "success": "send to %s success." % kwargs["receiver"],
            "code": http_code.OK
        }
        message = json.dumps(message)
    except STPHTTPException as e:
        logger.debug("POST /email/v1/code - %s" % e.httpcode)
        logger.error("send code email ERROR:\n%s" % traceback.format_exc())
        message = {
            "error": "send mail failed.",
            "code": e.httpcode
        }
        message = json.dumps(message)
        return message, e.httpcode
    except json.decoder.JSONDecodeError:
        logger.error("register user ERROR: JSON decode failed.\n %s" %
                     traceback.format_exc())
        logger.debug("POST /user/v1/register - 406")
        message = {
            "error": "invalid POST request: JSON decode failed.",
            "code": http_code.NotAcceptable
        }
        message = json.dumps(message)
        return message, http_code.NotAcceptable

    return message, http_code.OK
