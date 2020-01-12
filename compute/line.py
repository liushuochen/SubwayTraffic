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


def line_list():
    all_line = []
    for line_name in lines:
        line_instance = lines[line_name]
        subway_line = {}
        subway_line["name"] = line_instance.name
        subway_line["uuid"] = line_instance.uuid
        all_line.append(subway_line)
    return all_line


def delete_line(uuid):
    for subway_line in lines:
        if lines[subway_line].uuid == uuid:
            lines.pop(subway_line)
            break
