"It contains only Controller instance"


class Controller:
    "It's responsible for controlling whole server functionality"
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.standards = {}
        self.system = type('', (), {})()
        self.systems_interfaces = {}
        self.chassis = type('', (), {})()
        self.chassis_interfaces = []
