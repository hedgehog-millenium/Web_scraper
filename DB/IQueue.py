
class IQueue:
    def push(self, _id):
        raise NotImplementedError()

    def pop(self):
        raise NotImplementedError()

    def peek(self):
        raise NotImplementedError()

    def complete(self, _id):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()