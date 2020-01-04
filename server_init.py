"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system init.
"""

from api.system import system_blue
from api.line import line_blue
from api.user import user_blue
from api.email import email_blue
from api.station import station_blue


def register(app):
    blue_prints = [
        system_blue,
        line_blue,
        user_blue,
        email_blue,
        station_blue
    ]

    for blue_print in blue_prints:
        app.register_blueprint(blue_print)
    return
