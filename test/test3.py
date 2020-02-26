demo = "old"


def change():
    global demo
    demo = "new"
    return


if __name__ == '__main__':
    print(demo)
    change()
    print(demo)