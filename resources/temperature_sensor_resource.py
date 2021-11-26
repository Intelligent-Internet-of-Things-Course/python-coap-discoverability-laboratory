import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
from model.temperature_sensor import TemperatureSensorDescriptor
from kpn_senml import *


class TemperatureSensorResource(resource.Resource):

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.temperature_sensor = TemperatureSensorDescriptor()
        self.if_ = "core.s"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.sensor.temperature"
        self.title = "Temperature Sensor"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        temp = SenmlRecord("temperature-sensor",
                           unit=SenmlUnits.SENML_UNIT_DEGREES_CELSIUS,
                           value=self.temperature_sensor.value,
                           time=int(time.time()))
        pack.add(temp)
        return pack.to_json()

    async def render_get(self, request):
        print("TemperatureSensorResource -> GET Request Received ...")
        print("TemperatureSensorResource -> Reading updated temperature value ...")
        self.temperature_sensor.measure_temperature()
        print("TemperatureSensorResource -> Updated Temperature Value: %f" % self.temperature_sensor.value)

        payload_string = self.build_senml_json_payload()

        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'], payload=payload_string.encode('utf8'))