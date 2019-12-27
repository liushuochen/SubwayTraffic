import hashlib

if __name__ == '__main__':
    demo_pwd = "zaq12wsx"
    hl = hashlib.md5()
    hl.update(demo_pwd.encode(encoding="utf-8"))
    md5_code = hl.hexdigest()
    print(md5_code)

    input_str = "e6a52c828d56b46129fbf85c4cd164b3"
    if input_str == md5_code:
        print("equal")
    else:
        print("not equal")

