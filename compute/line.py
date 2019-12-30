"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/29
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system compute for line.
"""

lines = {}


class Line(object):
    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.uuid = kwargs["uuid"]
        self.next = None
