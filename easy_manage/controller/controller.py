"It contains only Controller instance"
from easy_manage.systems.abstract_system import AbstractSystem


class Controller:
    "It's responsible for controlling whole server functionality"
    def __init__(self, name, description, db):
        self.name = name
        self.description = description
        self.db = db
        self.standards = {}
        self.connectors = []
        self.system = AbstractSystem(abstract=True)
        self.systems_interfaces = {}
        self.chassis_interfaces = []
