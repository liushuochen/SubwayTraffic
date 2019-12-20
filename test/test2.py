import db.user

if __name__ == '__main__':
    result = db.user.get_user_detail("gaoxiangyucc@qq.com")
    print(result, type(result))