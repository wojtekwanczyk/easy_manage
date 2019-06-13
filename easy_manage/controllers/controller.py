from datetime import datetime
from sshtunnel import SSHTunnelForwarder


class Controller:
    def __init__(self, name, address, port, tunnel=None):
        self.name = name
        self.address = address
        self.port = port
        self.last_update = datetime.now()
        if tunnel:
            self.open_tunnel(tunnel['address'], tunnel['username'], tunnel['password'])

    def open_tunnel(self, tunnelend_addres, username, password, ):
        self.tunnel = SSHTunnelForwarder(
            ssh_address_or_host=(tunnelend_addres, 22),
            remote_bind_address=(self.address, int(self.port)),
            ssh_username=username,
            ssh_password=password,
        )
        self.tunnel.start()
        self.port = self.tunnel.local_bind_address[1]
        self.address = self.tunnel.local_bind_address[0]
        print('Tunneled')

    def close_tunnel(self):
        self.tunnel.stop()
