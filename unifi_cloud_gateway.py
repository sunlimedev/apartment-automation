import ssl
import json
import http.client


class UnifiCloudGateway:
    """
    This class creates an interface for the Unifi API.
    With just the API key to your Unifi Console, info for all API calls is gathered.
    To create an API key, go to Network -> Integrations -> Create New API Key.

    Functions:
    get_connected_clients: Returns key-value pairs of connected clients with MAC address and IP address.
    client_mac_present: Returns true/false if passed MAC address is connected to Unifi Console.
    """
    def __init__(self, gateway_mac, gateway_ip, api_key, cert):
        self.mac = gateway_mac
        self.ip = gateway_ip
        self.headers = {'Accept': 'application/json',
                        'X-API-Key': f"{api_key}"}

        # create a connection with gateway IP and certificate
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cert)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        self.conn = http.client.HTTPSConnection(gateway_ip, context=context)

        # api call to get site ID
        self.conn.request(method='GET',
                          url='/proxy/network/integration/v1/sites',
                          headers=self.headers)
        response = self.conn.getresponse()
        data = response.read()
        parsed = json.loads(data)
        self.site_id = parsed.get('data')[0].get('id')

    def get_connected_clients(self):
        # GET request for information of all connected clients
        self.conn.request(method='GET',
                                  url=f"/proxy/network/integration/v1/sites/{self.site_id}/clients",
                                  headers=self.headers)

        # format response from gateway
        response = self.conn.getresponse()
        data = response.read()
        parsed = json.loads(data)

        # create MAC:IP dictionary for all connected clients
        clients = {self.mac : self.ip}
        for device in parsed.get('data', []):
            mac = device.get('macAddress')
            ip = device.get('ipAddress')
            if mac and ip:
                clients[mac] = ip

        return clients

    def client_mac_present(self, client_mac_address):
        # get MAC and IP addresses of connected clients
        clients = self.get_connected_clients()

        if client_mac_address in clients:
            connected = True
        else:
            connected = False

        return connected