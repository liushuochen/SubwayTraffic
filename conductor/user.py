"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/13
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system conductor for user.
"""

import db.user

def users():
    user_list = db.user.get_all_user_detail()
    print(user_list)
    for user in user_list:
        if user["username"] == "admin":
            user_list.remove(user)
            break

    return user_list