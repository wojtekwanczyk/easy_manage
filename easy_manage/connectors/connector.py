class Connector:
    def __init__(self, name, address, credentials, port):
        self.name = name
        self.address = address
        self.port = port
        self.url = 'https://' + self.address
        self.data = {}
        self.last_update = None
        self.credentials = credentials
