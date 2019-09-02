"Module with class responsible for abstraction over systems"

from easy_manage.controller.abstract import Abstract


class AbstractSystem(Abstract):
    "Class that represents the system and defines its methods"

    def __init__(self, name=None, connector=None, abstract=False):
        super().__init__(abstract)

        self.name = name
        self.connector = connector
        self.data = {}
        self.last_update = None

    def get_power_state(self):
        raise NotImplementedError

    def get_system_health(self):
        raise NotImplementedError
