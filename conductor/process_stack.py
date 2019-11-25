"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/25
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system process stack
                    operation.
"""

class Stack():
    def __init__(self):
        self.base = []

    def size(self):
        return len(self.base)

    def empty(self):
        return self.size() == 0

    def push(self, data):
        self.base.append(data)

    def pop(self):
        if self.size() <= 0:
            return
        else:
            return self.base.pop()


class ProStack(Stack):
    def push(self, process_id):
        if process_id in self.base:
            return
        self.base.append(process_id)