"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/11
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system database driver.
"""

import configparser
import mysql.connector
import util
from errors.HTTPcode import STPHTTPException

root_path = util.get_root_path()
url = root_path + "/conf/platform.conf"
print(url)
conf = configparser.ConfigParser()
conf.read(url)
username = conf.get("database", "username")
password = conf.get("database", "password")

mysql_db = mysql.connector.connect(
    host="localhost",
    user=username,
    password=password,
    database="subway"
)

db_cursor = mysql_db.cursor()


def get_all_user_detail():
    sql = "select * from user"
    db_cursor.execute(sql)
    db_data = db_cursor.fetchall()
    data = []
    for pre_db_data in db_data:
        pre_data = {}
        pre_data["username"] = pre_db_data[0]
        pre_data["password"] = pre_db_data[1]
        pre_data["token"] = pre_db_data[2]
        data.append(pre_data)
    return data

def get_all_username():
    data = get_all_user_detail()
    usernames = []
    for user in data:
        usernames.append(user["username"])
    return usernames

# if a invalid username, return a empty list `[]`
def get_user_detail(username):
    sql = "select * from user where username=\"%s\"" % username
    db_cursor.execute(sql)
    data = db_cursor.fetchall()
    if not data:
        raise STPHTTPException("can not find user %s" % username, 404)
    user_details = data[0]
    return user_details

# if username is a invalid username, update_token can not raise any errors
def update_token(username, token):
    sql =  "update user set token=\"%s\" where username=\"%s\"" % \
           (token, username)
    db_cursor.execute(sql)
    mysql_db.commit()
    return