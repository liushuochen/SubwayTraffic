"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/12/29
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system compute init
"""

import compute.line


def init(**kwargs):
    line_list = kwargs["lines"]
    for subway_line in line_list:
        instance = compute.line.Line(**subway_line)
        compute.line.lines[instance.name] = instance
    return
