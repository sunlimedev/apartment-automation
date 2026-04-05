# This file controls the Philips Hue bulbs around my apartment. If my phone is connected to my home network, then I am
# present, and the scheduled lighting should play. If my phone is not connected to the network, then I have left my
# apartment, and the lighting should be off to save power. mood_lighting.py implements this functionality with the
# systemd service, mood_lighting.service.


from time import sleep
from constants import UNIFI_GATEWAY_MAC, UNIFI_GATEWAY_IP, UNIFI_API_KEY, CERTIFICATE_NAME
from constants import IPHONE_MAC_ADDRESS, HUE_BRIDGE_MAC_ADDRESS
from unifi_cloud_gateway import UnifiCloudGateway
from philips_hue import create_bridge


def main():
    # create gateway instance
    gateway = UnifiCloudGateway(api_key=UNIFI_API_KEY,
                                gateway_mac=UNIFI_GATEWAY_MAC,
                                gateway_ip=UNIFI_GATEWAY_IP,
                                cert=CERTIFICATE_NAME)

    # get MAC and IP addresses of connected clients
    clients = gateway.get_connected_clients()

    # get bridge instance
    bridge = create_bridge(clients[HUE_BRIDGE_MAC_ADDRESS])

    lights = bridge.lights

    for light in lights:
        print(light.name)
        print(light.hue)
        print(light.colortemp)
        print(light.brightness)
        print(light.saturation)

    # loop to set lights
    while True:
        if gateway.client_mac_present(IPHONE_MAC_ADDRESS):
            for i in range(1, 4):
                if not bridge.get_light(i, 'on'):
                    bridge.set_light(i, 'on', True)
        else:
            for i in range(1, 4):
                if bridge.get_light(i, 'on'):
                    bridge.set_light(i, 'on', False)

        sleep(60)


if __name__ == '__main__':
    main()