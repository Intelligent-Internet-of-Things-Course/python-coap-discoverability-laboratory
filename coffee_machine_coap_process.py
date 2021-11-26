import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
from resources.temperature_sensor_resource import TemperatureSensorResource
from resources.coffee_actuator_resource import CoffeeActuatorResource
from resources.capsule_presence_sensor_resource import CapsulePresenceSensorResource

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.INFO)
# logging.getLogger("coap-server").setLevel(logging.DEBUG)


def main():

    device_name = "coffee-machine-0001"

    # Resource tree creation
    root = resource.Site()

    root.add_resource(['.well-known', 'core'], resource.WKCResource(root.get_resources_as_linkheader, impl_info=None))
    root.add_resource(['temperature'], TemperatureSensorResource(device_name))
    root.add_resource(['capsule'], CapsulePresenceSensorResource(device_name))
    root.add_resource(['coffee'], CoffeeActuatorResource(device_name))
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683)))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
