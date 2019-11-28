"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/25
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor init
"""

import os
import util
from conductor.process_stack import ProStack
from logs.logger import LOG
from multiprocessing import Queue

log_path = util.get_log_path()
logger = LOG(
    model="a",
    path=log_path,
    name="conductor"
)

process_stack = ProStack()
process_queue = Queue()

def init():
    logger.info("init conductor...")
    process_stack.push(os.getpid())
