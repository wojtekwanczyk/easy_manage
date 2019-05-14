class Controller:
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        self.socket = ':'.join([address, port])
        self.url = 'http://' + self.socket
