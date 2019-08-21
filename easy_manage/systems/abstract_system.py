class AbstractSystem:
    "Class that represents the system and defines its methods"

    def __init__(self, name, connector):
        self.name = name
        self.connector = connector
        self.db = connector.db
        self.data = {}
        self.last_update = None

    def get_power_state(self):
        pass

    def get_system_health(self):
        pass
