class AbstractSystem:
    """Class that represents the system and defines its methods"""

    def __init__(self, name, connector):
        self.name = name
        self.connector = connector
        self.data = {}
        self.last_update = None
        self.methods = ['get_power_state', 'get_status']

    def __dir__(self):
        return []

    def get_power_state(self):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError
