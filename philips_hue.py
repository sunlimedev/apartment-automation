from phue import Bridge, PhueRegistrationException, PhueRequestTimeout


def create_bridge(hue_bridge_ip):
    # create a philips hue bridge class instance with bridge IP
    try:
        bridge = Bridge(hue_bridge_ip)
        bridge.connect()
    except PhueRegistrationException as e:
        print('Press the button on the bridge and try again')
        raise e
    except PhueRequestTimeout as e:
        print('Could not connect to the bridge - check your network')
        raise e

    return bridge

