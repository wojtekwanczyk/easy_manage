from datetime import datetime
from easy_manage.controllers.RedfishController import RedfishController


class AbstractSystem:
    "Class that represents the system and defines its methods"

    def __init__(self, name, controller):
        self.name = name
        self.controller = controller
        self.db = controller.db
        self.data = {}
    
    def get_power_state(self):
        pass

    def get_status(self):
        pass
