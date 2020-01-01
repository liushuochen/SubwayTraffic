"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/27
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system subway station operate api
"""

import flask

station_blue = flask.Blueprint("station_blue", __name__, url_prefix="/station/v1")


@station_blue.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Headers',
                     'Content-Type,Authorization,session_id')
    resp.headers.add('Access-Control-Allow-Methods',
                     'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@station_blue.route("/add", methods=["POST"])
def add_station():
    pass
