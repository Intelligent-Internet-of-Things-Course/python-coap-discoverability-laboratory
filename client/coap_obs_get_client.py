import logging
import asyncio
import aiocoap
from aiocoap import *

logging.basicConfig(level=logging.INFO)


async def main():
    protocol = await Context.create_client_context()

    request = Message(code=aiocoap.GET, uri='coap://127.0.0.1:5683/coffee', observe=0)

    protocol_request = protocol.request(request)

    r = await protocol_request.response
    print("First response: %s\n%r" % (r, r.payload))

    received_observation = 0

    async for r in protocol_request.observation:
        print("Next result: %s\n%r" % (r, r.payload))
        received_observation += 1
        if received_observation == 10:
            print("Canceling Observation ...")
            protocol_request.observation.cancel()
            break

    await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
