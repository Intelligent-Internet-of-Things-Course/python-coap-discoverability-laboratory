import aiocoap.resource as resource
import aiocoap
import aiocoap.numbers as numbers
import time
import json
from aiocoap.numbers.codes import Code
from model.coffee_history import CoffeeHistoryDescriptor
from request.make_coffee_request import MakeCoffeeRequestDescriptor
from kpn_senml import *


class CoffeeActuatorResource(resource.ObservableResource):
    """Example resources that can be observed. The `notify` method keeps
    scheduling itself, and calles `update_state` to trigger sending
    notifications."""

    def __init__(self, device_name):
        super().__init__()
        self.device_name = device_name
        self.coffee_history = CoffeeHistoryDescriptor()
        self.if_ = "core.a"
        self.ct = numbers.media_types_rev['application/senml+json']
        self.rt = "it.unimore.device.actuator.coffee"
        self.title = "Coffee Actuator"

    def build_senml_json_payload(self):
        pack = SenmlPack(self.device_name)
        pack.base_time = int(time.time())
        pack.base_unit = SenmlUnits.SENML_UNIT_COUNTER
        short = SenmlRecord("short_coffee",
                            value=self.coffee_history.shortCount)

        medium = SenmlRecord("medium_coffee",
                             value=self.coffee_history.shortCount)

        long = SenmlRecord("long_coffee",
                           value=self.coffee_history.shortCount)

        total = SenmlRecord("totale_coffee",
                           value=self.coffee_history.totalCount)

        pack.add(short)
        pack.add(medium)
        pack.add(long)
        pack.add(total)

        return pack.to_json()

    async def render_get(self, request):
        print("CoffeeActuatorResource -> GET Request Received ...")
        payload_string = self.build_senml_json_payload()
        return aiocoap.Message(content_format=numbers.media_types_rev['application/senml+json'], payload=payload_string.encode('utf8'))

    async def render_post(self, request):
        print("CoffeeActuatorResource -> POST Request Received ...")
        self.coffee_history.increase_short_coffee()
        self.updated_state()
        return aiocoap.Message(code=Code.CHANGED)

    async def render_put(self, request):
        print('CoffeeActuatorResource -> PUT Byte payload: %s' % request.payload)
        json_payload_string = request.payload.decode('UTF-8')
        print('CoffeeActuatorResource -> PUT String Payload: %s' % json_payload_string)
        make_coffee_request = MakeCoffeeRequestDescriptor(**json.loads(json_payload_string))
        print('Coffee Type Request Received: %s' % make_coffee_request.type)
        if make_coffee_request.type == MakeCoffeeRequestDescriptor.COFFEE_TYPE_SHORT:
            self.coffee_history.increase_short_coffee()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        elif make_coffee_request.type == MakeCoffeeRequestDescriptor.COFFEE_TYPE_MEDIUM:
            self.coffee_history.increase_medium_coffee()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        elif make_coffee_request.type == MakeCoffeeRequestDescriptor.COFFEE_TYPE_LONG:
            self.coffee_history.increase_long_coffee()
            self.updated_state()
            return aiocoap.Message(code=Code.CHANGED)
        else:
            return aiocoap.Message(code=Code.BAD_REQUEST)
