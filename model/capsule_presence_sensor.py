import random
import json
import time


class CapsulePresenceSensorDescriptor:

    def __init__(self):
        self.value = False
        self.timestamp = 0
        self.check_capsule_presence()

    def check_capsule_presence(self):
        self.value = bool(random.getrandbits(1))
        self.timestamp = int(time.time())

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)