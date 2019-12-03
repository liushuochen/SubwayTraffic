"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system entrance.
"""

import flask
import configparser
import datetime
import api.system as system
import api.user as user
import api.line as line
import db
import logs
import conductor
from api import logger

stp_app = flask.Flask("SubwayTraffic")
stp_app.register_blueprint(system.system_blue)
stp_app.register_blueprint(user.user_blue)
stp_app.register_blueprint(line.line_blue)


def init():
    conductor.init()
    logs.init()

    # if host mysql server do not start, db.init() will raise
    # mysql.connector.errors.InterfaceError.
    db.init()


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("conf/platform.conf")
    host = conf.get("system", "host")
    port = conf.get("system", "port")
    session_key = conf.get("system", "session_key")

    stp_app.secret_key = session_key
    stp_app.permanent_session_lifetime = datetime.timedelta(hours=1)

    init()

    logger.info("=" * 23)
    logger.info("Service starting....")
    stp_app.run(host=host, port=port)