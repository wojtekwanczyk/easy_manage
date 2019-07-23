class Controller:

    def __init__(self, name, description, db):
        self.name = name
        self.description = description
        self.db = db
        self.standards = {}
        self.connectors = []
        self.system = AbstractInstance()
        self.systems_interfaces = {}
        self.chassis_interfaces = []


class AbstractInstance:
    def __init__(self):
        self.methods = []

    def __dir__(self):
        return []
