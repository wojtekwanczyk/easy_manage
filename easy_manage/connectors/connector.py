class Connector():
    def __init__(self, name, address, db, credentials, port):
        self.name = name
        self.address = address
        self.db = db
        self.port = port
        self.url = 'https://' + self.address
        self.data = {}
        self.last_update = None
        self.credentials = credentials
