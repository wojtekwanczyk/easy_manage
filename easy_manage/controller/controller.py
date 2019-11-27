"It contains only Controller instance"


class Controller():
    "It's responsible for controlling whole server functionality"
    def __init__(self):
        self.standards = {}
        self.components = {}
        self.system = type('System', (), {})()
        self.chassis = type('Chassis', (), {})()
        self.shell = type('Shell', (), {})()
