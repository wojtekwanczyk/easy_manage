"Module which describes abstract chassis class"

class AbstractChassis:
    "Class that represents the chassis and defines its methods"

    def __init__(self, name, connector):
        self.name = name
        self.connector = connector
        self.db = connector.db
        self.data = {}
        self.last_update = None
        
    def get_power_state(self):
        pass

    def get_health(self):
        pass
