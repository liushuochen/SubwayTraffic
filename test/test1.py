import conductor
import test.test2

if __name__ == '__main__':
    print(conductor.process.base)
    conductor.init()
    print(conductor.process.base)
    test.test2.demo()
    print(conductor.process.base)