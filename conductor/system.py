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


def update_token(username):
    new_token = general_token()
    model.update_token(username, new_token)
    return


def verify_user(post_username, post_password):
    try:
        _, password, token, _ = model.get_user_detail(post_username)
        if post_password != password:
            logger.error("user %s can not login: Wrong username or password.")
            raise STPHTTPException("Wrong username or password.", 403)
        return token
    except DBError as e:
        raise STPHTTPException(e.error_message, e.error_code)


def general_token():
    new_token_list = []
    for i in range(TOKEN_LENGTH):
        new_token_list.append(random.choice(pools))
    new_token = "".join(new_token_list)
    return new_token