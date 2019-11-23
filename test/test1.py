import test.test2

class TQueue():
    def __init__(self):
        self.base = []

    def add(self, ele):
        self.base.append(ele)

    def show(self):
        return self.base

a = TQueue()

if __name__ == '__main__':
    print(a.show())
    test.test2.add_a(a)
    print(a.show())