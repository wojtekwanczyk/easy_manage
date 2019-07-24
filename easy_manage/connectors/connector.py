class Connector:
    "Abstract class that all interfaces connectors inheritance from"
    def __init__(self, name, address, credentials, port):
        self.name = name
        self.address = address
        self.port = port
        self.last_update = None
        self.credentials = credentials
