"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor for system
                    operation.
"""

import util
import db.user as model
import random
import string
import traceback
from errors.HTTPcode import STPHTTPException, DBError
from conductor import logger

pools = string.ascii_letters + string.digits
TOKEN_LENGTH = 10

def get_version():
    root_path = util.get_root_path()
    url = root_path + "/conf/stp.version"
    try:
        version = open(url, "r").read()
    except FileNotFoundError:
        logger.error("get version failed. can not find version file.\n %s" %
                     traceback.format_exc())
        raise STPHTTPException("can not found file: stp.version", 503)
    return version


def get_token(username):
    details = model.get_user_detail(username)[0]
    token = details[2]
    return token


def update_token(email):
    new_token = general_token()
    model.update_token(email, new_token)
    return


def verify_user(post_email, post_password):
    try:
        detail = model.get_user_detail(post_email)
        password = detail[3]
        token = detail[4]
        if post_password != password:
            logger.error("user %s can not login: Wrong email or password." %
                         post_email)
            raise STPHTTPException("Wrong email or password.", 404)
        return token
    except DBError as e:
        raise STPHTTPException(e.error_message, e.error_code)


def general_token():
    new_token_list = []
    for i in range(TOKEN_LENGTH):
        new_token_list.append(random.choice(pools))
    new_token = "".join(new_token_list)
    return new_token