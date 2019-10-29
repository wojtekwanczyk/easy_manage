"Module containing class responsible for connection with remote device(s)"


class Connector():
    "Class responsible for connection with remote device(s)"

    def __init__(self, name, address, credentials, port):
        self.name = name
        self.address = address
        self.port = port
        self.credentials = credentials

    def test_connection(self):
        raise NotImplementedError
