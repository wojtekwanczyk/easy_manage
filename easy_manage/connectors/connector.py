"Module containing class responsible for connection with remote device(s)"


class Connector:
    "Class responsible for connection with remote device(s)"

    def __init__(self, address, credentials, port):
        self.address = address
        self.port = port
        self.credentials = credentials
        self.connected = False

    def test_connection(self):
        raise NotImplementedError

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError
