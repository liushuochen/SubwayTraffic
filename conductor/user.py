"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system conductor for user.
"""

import db.user

def users():
    user_list = db.user.get_all_username()
    if "admin" in user_list:
        user_list.remove("admin")

    return user_list