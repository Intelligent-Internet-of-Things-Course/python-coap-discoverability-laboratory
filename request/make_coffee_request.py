import json


class MakeCoffeeRequestDescriptor:

    COFFEE_TYPE_SHORT = "short_coffee"
    COFFEE_TYPE_MEDIUM = "medium_coffee"
    COFFEE_TYPE_LONG = "long_coffee"

    def __init__(self, type):
        self.type = type

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)