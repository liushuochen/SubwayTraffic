def demo():
    url = "/root/image/localhost/default.jpeg"
    url_list = url.rsplit("/", 1)
    return url_list[0], url_list[1]


if __name__ == '__main__':
    path, file = demo()
    print(path, file)
