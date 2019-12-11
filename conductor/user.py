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
from conductor import logger

user_security_password_length = 8

admin = 1
user = 2

def users():
    user_list = db.user.get_all_user_detail()
    for user in user_list:
        if user["username"] == "admin":
            user_list.remove(user)
            break

    logger.info("Get user list: %s" % user_list)
    return user_list


def register(**kwargs):
    email_set = available_email()
    if kwargs["email"] in email_set:
        raise STPHTTPException("The email %s already exist"
                               % kwargs["email"], 403)
    if len(kwargs["password"]) < user_security_password_length:
        raise STPHTTPException("Password length must more than 8.", 403)

    try:
        kwargs["uuid"] = util.generate_uuid()
        kwargs["token"] = conductor.system.general_token()
        kwargs["register_time"] = util.get_time_string_format()
        db.user.add_user(**kwargs)
    except Exception as e:
        raise STPHTTPException("Register user ERROR: %s" % str(e), 503)
    return


def available_email():
    user_list = db.user.get_all_user_detail()
    email = set()
    for user in user_list:
        email.add(user["email"])
    return email


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


def modify_user_pwd(username, password, new_password):
    conductor.system.verify_user(username, password)

    if len(new_password) < User_security_password_length:
        logger.error("Change user %s password ERROR: Password length must more than"
                     " 8." % username)
        raise STPHTTPException("Password length must more than 8.", 403)

    db.user.update_pwd(username, new_password)
    logger.info("Change user %s password successful." % username)
    return


def check_email(email):
    if email.count("@") != 1 or email[-4:] != ".com":
        raise STPHTTPException("Invalid email format %s." % email, 400)
