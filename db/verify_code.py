# SubwayTraffic Platform
# Description: 
# File: verify_code
# Date: 2020/2/23 - 19:39

import db.engine
from db import logger


def init_verify_code():
    engine, cursor = db.engine.get_engine()
    sql = """
        create table if not exists verify_code(
        uuid    char(27),
        code    varchar(10) not null,
        operate varchar(20) not null,
        modify  datetime not null,
        primary key(uuid)
        ) charset utf8
        """
    cursor.execute(sql)
    engine.close()
    logger.info("setup verify code finished.")
    return
