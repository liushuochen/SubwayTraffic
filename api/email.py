"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/25
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system process send email
                    operation.
"""

import flask
import random
import json

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
    pools = "0123456789"
    code = ""
    while True:
        number = random.choice(pools)
        code = code + number
        if len(code) >= 6:
            break

    kwargs = {
        "header": header,
        "type": "send_code",
        "receiver": receiver,
        "operate": operate,
        "code": code
    }
    import main
    main.send_mail(**kwargs)

    message = {
        "success": "send to %s success." % receiver,
        "code": 200
    }
    message = json.dumps(message)
    return message, 200
