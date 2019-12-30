"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system entrance.
"""

import flask
import flask_mail
import configparser
import db
import logs
import conductor
import server_init
import util
import compute
from api import logger

conf = configparser.ConfigParser()
config_path = util.get_root_path() + "/conf/platform.conf"
conf.read(config_path)
host = conf.get("system", "host")
port = conf.get("system", "port")

stp_app = flask.Flask("SubwayTraffic")
stp_app.config.update(
    MAIL_SERVER="smtp.qq.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=conf.get("deploy", "admin_email"),
    MAIL_PASSWORD=conf.get("deploy", "admin_email_pwd"),
)
stp_email = flask_mail.Mail(stp_app)

server_init.register(stp_app)


def send_mail(**kwargs):
    subject = kwargs["header"]
    mail_type = kwargs["type"]
    message = flask_mail.Message(
        subject,
        recipients=kwargs["receiver"],
        sender=("SubwayTraffic", conf.get("deploy", "admin_email")),
    )
    if mail_type == "send_code":
        message.html = flask.render_template("send_code.html",
                                             operate=kwargs["operate"],
                                             code=kwargs["code"])
        stp_email.send(message)
    else:
        raise TypeError("invalid email type: %s." % mail_type)
    return


def init():
    conductor.init()
    logs.init()

    # TODO: if host mysql server do not start, db.init() will raise
    # mysql.connector.errors.InterfaceError.
    lines = db.init()
    compute.init(lines=lines)


if __name__ == '__main__':
    init()

    logger.info("=" * 23)
    logger.info("Service starting....")
    stp_app.run(host=host, port=port)
