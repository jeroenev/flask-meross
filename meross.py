import asyncio
import os

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

EMAIL = os.environ.get('MEROSS_EMAIL') or "DEFAULT_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "DEFAULT_PASS"

async def meross_action(name="phonecharger", action="off"):
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS310 devices that are registered on this account
    await manager.async_device_discovery()
    devices = manager.find_devices(device_type="mss210")
    if len(devices) < 1:
        print("No MSS210 plugs found...")
    else:
        for plug in devices:
            if name in plug._name:
                # Turn it on channel 0
                # plug_name = plugs[0]._name = "bedroom charger"
                
                # Update device status: this is needed only the very first time we play with this device (or if the
                #  connection goes down)
                await plug.async_update()
                if action == "on":
                    print(f"Turning on {plug.name}...")
                    await plug.async_turn_on(channel=0)
                elif action == "off":
                    print(f"Turing off {plug.name}")
                    await plug.async_turn_off(channel=0)
    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()
        


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(meross_action())
    loop.close()