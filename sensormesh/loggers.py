class Logger(object):
    def __init__(self):
        pass

    def add(self, measurement):
        pass


class ConsoleLogger(Logger):
    def __init__(self):
        super().__init__()

    def add(self, measurement):
        print(measurement)
