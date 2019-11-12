"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system entrance.
"""

import flask
import configparser
import datetime
import api.system as system

stp_app = flask.Flask("SubwayTraffic")
stp_app.register_blueprint(system.system_blue)

if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read("conf/platform.conf")
    host = conf.get("system", "host")
    port = conf.get("system", "port")

    stp_app.secret_key = "qwerasdf@2019"
    stp_app.permanent_session_lifetime = datetime.timedelta(hours=1)

    stp_app.run(host=host, port=port)