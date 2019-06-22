from datetime import datetime


class Controller:
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        self.url = 'https://' + self.address
        self.last_update = datetime.now()
