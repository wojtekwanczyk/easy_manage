from easy_manage.systems.abstract_system import AbstractSystem


class Controller:

    def __init__(self, name, description, db):
        self.name = name
        self.description = description
        self.db = db
        self.standards = {}
        self.connectors = []
        self.system = AbstractSystem(None, None)  # TODO dir should be overridden that it returns nothing
        self.systems_interfaces = {}
        self.chassis_interfaces = []
