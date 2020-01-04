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
            "subway station %s has been exit." % kwargs["name"],
            403,
            10300
        )
    kwargs["uuid"] = util.generate_uuid(uuid_type="upper")
    db.station.add_station(**kwargs)
    return
