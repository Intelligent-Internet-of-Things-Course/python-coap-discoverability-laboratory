import json


class CoffeeHistoryDescriptor:

    def __init__(self):
        self.totalCount = 0
        self.shortCount = 0
        self.mediumCount = 0
        self.longCount = 0

    def increase_long_coffee(self):
        self.totalCount += 1
        self.longCount += 1

    def increase_medium_coffee(self):
        self.totalCount += 1
        self.mediumCount += 1

    def increase_short_coffee(self):
        self.totalCount += 1
        self.shortCount += 1

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
