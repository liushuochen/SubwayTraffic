
def deo(func):
    def wapper(*args, **kwargs):
        print("deo")
        func(*args, **kwargs)
        return
    return wapper

@deo
def demo1():
    print("demo1")

if __name__ == '__main__':
    demo1()
