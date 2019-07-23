"Module containing class responsible for connection with remote device(s)"


class Connector():
    "Class responsible for connection with remote device(s)"

    def __init__(self, name, address, db, credentials, port):
        self.name = name
        self.address = address
        self.db = db
        self.port = port
        self.url = 'https://' + self.address
        self.data = {}
        self.last_update = None
        self.credentials = credentials
