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
import api.system as system
import api.user as user
import api.line as line
import api.email as semail
import db
import logs
import conductor
from api import logger

conf = configparser.ConfigParser()
conf.read("conf/platform.conf")
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

stp_app.register_blueprint(system.system_blue)
stp_app.register_blueprint(user.user_blue)
stp_app.register_blueprint(line.line_blue)
stp_app.register_blueprint(semail.email_blue)


def send_mail(**kwargs):
    subject = kwargs["header"]
    mail_type = kwargs["type"]
    message = flask_mail.Message(
        subject,
        recipients=kwargs["receiver"],
        sender=("admin", conf.get("deploy", "admin_email")),
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

    # if host mysql server do not start, db.init() will raise
    # mysql.connector.errors.InterfaceError.
    db.init()


if __name__ == '__main__':
    init()

    logger.info("=" * 23)
    logger.info("Service starting....")
    stp_app.run(host=host, port=port)
