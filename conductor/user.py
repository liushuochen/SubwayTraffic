"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor for user.
"""

import db.user
import conductor.system
import util
from errors.HTTPcode import STPHTTPException, DBError

User_security_password_length = 8

def users():
    user_list = db.user.get_all_user_detail()
    for user in user_list:
        if user["username"] == "admin":
            user_list.remove(user)
            break

    return user_list


def register(username, password):
    usernames = available_user()
    if username in usernames:
        raise STPHTTPException("The username %s already exist"
                               % username, 403)
    if len(password) < User_security_password_length:
        raise STPHTTPException("Password length must more than 8.", 403)

    try:
        token = conductor.system.general_token()
        register_time = util.get_time_string_format()
        db.user.add_user(username=username,
                         password=password,
                         register_time=register_time,
                         token=token)
    except Exception as e:
        raise STPHTTPException("Register user ERROR: %s" % str(e), 503)
    return


def available_user():
    user_list = db.user.get_all_user_detail()
    usernames = []
    for user in user_list:
        usernames.append(user["username"])
    return usernames


def destroy(username):
    usernames = available_user()
    if username not in usernames:
        raise STPHTTPException("can not find user %s" % username, 404)

    if username == "admin":
        raise STPHTTPException("can not delete admin user", 401)

    try:
        db.user.drop_user(username)
    except DBError as e:
        raise STPHTTPException(e.error_message, e.error_code)
    return