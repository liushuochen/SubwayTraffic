"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system conductor for user.
"""

import db.user
import datetime
import conductor.system
from errors.HTTPcode import STPHTTPException

User_security_password_length = 8

def users():
    user_list = db.user.get_all_user_detail()
    for user in user_list:
        if user["username"] == "admin":
            user_list.remove(user)
            break

    return user_list


def register(username, password):
    user_list = db.user.get_all_user_detail()
    usernames = []
    for user in user_list:
        usernames.append(user["username"])

    if username in usernames:
        raise STPHTTPException("The username %s already exist"
                               % username, 403)
    if len(password) < User_security_password_length:
        raise STPHTTPException("Password length must more than 8.", 403)

    try:
        token = conductor.system.general_token()
        register_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.user.add_user(username=username,
                         password=password,
                         register_time=register_time,
                         token=token)
    except Exception as e:
        raise STPHTTPException("Register user ERROR: %s" % str(e), 503)
    return