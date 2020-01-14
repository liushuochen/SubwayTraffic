"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2020/01/04
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor for station.
"""

import util
import db.station
from errors.HTTPcode import STPHTTPException


def add_station(**kwargs):
    if db.station.exist(kwargs["name"]):
        raise STPHTTPException(
            "subway station %s has been exist." % kwargs["name"],
            403,
            10300
        )
    kwargs["uuid"] = util.generate_uuid(uuid_type="upper")
    db.station.add_station(**kwargs)
    return


def delete(uuid):
    if not db.station.exist(uuid, types="uuid"):
        raise STPHTTPException(
            "subway station %s has not exist." % uuid,
            404,
            10301
        )

    station_detail = db.station.detail(uuid)
    if station_detail["belong"] is not None:
        raise STPHTTPException(
            "The subway station %s is in a bind." % uuid,
            403,
            10302
        )

    db.station.delete(uuid)
    return


def update(uuid, name):
    if not db.station.exist(uuid, types="uuid"):
        raise STPHTTPException(
            "subway station %s has not exist." % uuid,
            404,
            10301
        )

    station_detail = db.station.detail(uuid)
    if station_detail["belong"] is not None:
        raise STPHTTPException(
            "The subway station %s is in a bind." % uuid,
            403,
            10302
        )

    db.station.update(uuid, name)
    return
