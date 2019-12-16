"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system util tools.
"""

import os
import datetime
import configparser
import random
import string
from errors.HTTPcode import STPHTTPException


session = {}
TOKEN_LENGTH = 10
pools = string.ascii_letters + string.digits


def get_root_path():
    url_list = (os.path.abspath("")).split("/")
    url = ""
    for path in url_list:
        if path == "SubwayTraffic":
            url = url + path
            break
        url = url + path + "/"
    return url


# translate datetime.datetime to string.
# if time_data is None, func will return current time string format.
# time_date's type must be datetime.datetime
def get_time_string_format(time_data=None):
    if not time_data:
        time_string = \
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        time_string = time_data.strftime("%Y-%m-%d %H:%M:%S")
    return time_string


def get_log_path():
    conf_path = get_root_path() + "/conf/platform.conf"
    conf = configparser.ConfigParser()
    conf.read(conf_path)
    log_path = conf.get("logs", "log_path")
    return log_path


# generate a uuid string.
# if uuid_type is lower, generate a uuid like: aaaaaaaa-aaaa-aaaa-aaaaaaaa
# if uuid_type is upper, generate a uuid like: AAAAAAAA-AAAA-AAAA-AAAAAAAA
# otherwise function will raise TypeError.
def generate_uuid(uuid_type="lower"):
    if uuid_type == "lower":
        pools = string.digits + string.ascii_lowercase
    elif uuid_type == "upper":
        pools = string.digits + string.ascii_uppercase
    else:
        raise TypeError("Invalid uuid type %s." % uuid_type)

    random_char_list = []
    while len(random_char_list) < 27:
        length = len(random_char_list)
        if length == 8 or length == 13 or length == 18:
            random_char_list.append("-")
            continue
        random_char_list.append(random.choice(pools))
    uuid = "".join(random_char_list)
    return uuid


def check_param(**kwargs):
    for param in kwargs:
        if kwargs[param] is None:
            raise STPHTTPException("BadRequest: Invalid param %s request." %
                                   param, 400)
    return


def general_token():
    new_token_list = []
    for i in range(TOKEN_LENGTH):
        new_token_list.append(random.choice(pools))
    new_token = "".join(new_token_list)
    return new_token


def general_verify_code(length):
    number_pools = "0123456789"
    if length <= 0:
        return ""

    verify_code_list = []
    for i in range(length):
        verify_code_list.append(random.choice(number_pools))

    verify_code = "".join(verify_code_list)
    return verify_code

def admin_email():
    conf_path = get_root_path() + "/conf/platform.conf"
    conf = configparser.ConfigParser()
    conf.read(conf_path)
    email = conf.get("deploy", "admin_email")
    return email
