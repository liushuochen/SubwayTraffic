import db.user as model
import datetime

if __name__ == '__main__':
    u = model.get_all_user_detail()
    create = u[0]["create"]
    create_str = datetime.datetime.strftime(create, "%Y-%m-%d %H:%M:%S")
    print(create_str, type(create_str))