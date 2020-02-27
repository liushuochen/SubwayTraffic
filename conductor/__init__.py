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
from configparser import NoSectionError
from errors.service import StartException

log_path = util.get_log_path()
logger = LOG(
    model="a",
    path=log_path,
    name="conductor"
)

process_stack = ProStack()
process_queue = Queue()


def init():
    process_stack.push(os.getpid())
    try:
        _, _ = util.get_storage_detail(util.get_rsa_path())
    except NoSectionError:
        raise StartException("can not find rsa config file.")
    return

