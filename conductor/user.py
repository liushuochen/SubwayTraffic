"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system conductor for user.
"""

import db.user
import util
import datetime
from errors.HTTPcode import STPHTTPException, DBError
from conductor import logger

user_security_password_length = 8

admin = 1
normal_user = 2


def users():
    user_list = db.user.get_all_user_detail()
    admin_email = util.admin_email()
    for user in user_list:
        if user["email"] == admin_email:
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
        kwargs["token"] = util.general_token()
        kwargs["register_time"] = util.get_time_string_format()
        db.user.add_user(**kwargs)
    except Exception as e:
        raise STPHTTPException("Register user ERROR: %s" % str(e), 503)
    return


def available_email():
    user_list = db.user.get_all_user_detail()
    email = set()
    for user_detail in user_list:
        email.add(user_detail["email"])
    return email


def destroy(uuid):
    delete_user = user_detail(uuid)
    if delete_user["type"] == "admin":
        raise STPHTTPException("can not delete admin user.", 403)

    db.user.drop_user(uuid)
    return


def user_detail(uuid):
    user_list = db.user.get_all_user_detail()
    for user_message in user_list:
        if user_message["uuid"] == uuid:
            target_user = user_message
            break
    else:
        raise STPHTTPException("can not find user %s" % uuid, 404)

    return target_user


def update(**kwargs):
    email = kwargs["email"]
    username = db.user.get_user_detail(email)[2]
    kwargs["username"] = username
    user_uuid = db.user.get_user_detail(email)[0]
    uuid = kwargs["uuid"]
    if user_uuid != uuid:
        raise STPHTTPException("Invalid uuid %s" % uuid, 403)

    params = {"uuid": uuid}
    if "new_password" in kwargs:
        params["password"] = kwargs["new_password"]
    else:
        params["password"] = kwargs["password"]
    if len(params["password"]) < user_security_password_length:
        raise STPHTTPException("Password length must more than 8.", 403)

    if "new_email" in kwargs:
        params["email"] = kwargs["new_email"]
    else:
        params["email"] = kwargs["email"]
    check_email(params["email"])

    if "new_username" in kwargs:
        params["username"] = kwargs["new_username"]
    else:
        params["username"] = kwargs["username"]

    db.user.update(**params)
    logger.info("update user %s param: %s" % (params["uuid"], params))
    return


def check_email(email):
    if email.count("@") != 1 or email[-4:] != ".com":
        raise STPHTTPException("Invalid email format %s." % email, 400)


def is_admin_user(uuid):
    user = user_detail(uuid)
    return user["type"] == "admin"


def code_exit(uuid):
    return len(db.user.get_code_detail(uuid)) > 0


def push_verify_code(receiver, code, operate):
    for email in receiver:
        try:
            uuid = db.user.get_user_detail(email)[0]
            if code_exit(uuid):
                db.user.drop_code(uuid)
            modify_time = util.get_time_string_format()
            db.user.add_code(uuid, code, operate, modify_time)
        except DBError:
            continue
    return


def is_user_exist(email):
    result = db.user.is_user_exist(email)
    sample_detail = {"email": email, "exist": result}
    if result == 1:
        sample_detail["uuid"] = db.user.get_user_detail(email)[0]
    return sample_detail


def check_verify_code(**kwargs):
    detail = db.user.get_code_detail(kwargs["uuid"])
    if len(detail) <= 0:
        raise STPHTTPException("Can not find verification code for %s"
                               % kwargs["uuid"], 404)

    if kwargs["verify_code"] != detail[1]:
        raise STPHTTPException("Wrong verification code input.", 403)
    now = datetime.datetime.now()
    code_create_time = detail[3]
    if (now - code_create_time).seconds > 900:
        raise STPHTTPException("The verification code has expired", 408)
