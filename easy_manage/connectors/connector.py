"Module containing class responsible for connection with remote device(s)"


class Connector():
    "Class responsible for connection with remote device(s)"

    def __init__(self, name, address, credentials, port):
        self.name = name
        self.address = address
        self.port = port
        self.last_update = None
        self.credentials = credentials
