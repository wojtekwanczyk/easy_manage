from datetime import datetime


class Controller:
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        # TODO: Do we need below for both controllers?
        self.socket = ':'.join([address, port])
        self.url = 'http://' + self.socket
        self.last_update = datetime.now()
