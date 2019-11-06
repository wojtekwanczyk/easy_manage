"Module with class responsible for abstraction over systems"


class AbstractSystem:
    "Class that represents the system and defines its methods"

    def __init__(self, name=None, connector=None):
        super().__init__()

        self.name = name
        self.connector = connector
        self.data = {}
        self.last_update = None

    def get_power_state(self):
        raise NotImplementedError

    def get_system_health(self):
        raise NotImplementedError
