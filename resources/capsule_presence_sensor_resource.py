import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
from model.capsule_presence_sensor import CapsulePresenceSensorDescriptor
from kpn_senml import *


class CapsulePresenceSensorResource(resource.Resource):

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.sensor = CapsulePresenceSensorDescriptor()
        self.if_ = "core.s"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.sensor.capsule_presence"
        self.title = "Capsule Presence Sensor"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        capsule_presence = SenmlRecord("capsule",
                                       value=self.sensor.value,
                                       time=int(time.time()))
        pack.add(capsule_presence)
        return pack.to_json()

    async def render_get(self, request):
        print("CapsulePresenceResource -> GET Request Received ...")
        print("CapsulePresenceResource -> Check Capsule Presence ...")
        self.sensor.check_capsule_presence()
        print("CapsulePresenceResource -> Updated Capsule Presence Sensor Value: %f" % self.sensor.value)

        payload_string = self.build_senml_json_payload()

        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'], payload=payload_string.encode('utf8'))
