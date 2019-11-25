"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/25
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor init
"""

import os
from conductor.process_stack import ProStack

process = ProStack()

def init():
    process.push(os.getpid())