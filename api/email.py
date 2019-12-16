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
    data = json.loads(flask.request.data)

    receiver = data.get("receiver", None)
    header = data.get("header", None)
    operate = data.get("operate", None)
    verify_code = util.general_verify_code(6)
    kwargs = {
        "header": header,
        "type": "send_code",
        "receiver": receiver,
        "operate": operate,
        "code": verify_code
    }
    from main import send_mail
    send_mail(**kwargs)

    conductor.user.push_verify_code(receiver, verify_code, operate)

    message = {
        "success": "send to %s success." % receiver,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200
