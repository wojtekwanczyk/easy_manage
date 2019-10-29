"It contains only Controller instance"
from easy_manage.controller.abstract import ControllerTools


class Controller:
    "It's responsible for controlling whole server functionality"
    def __init__(self, name, description, db):
        self.name = name
        self.description = description
        self.db = db
        self.standards = {}
        self.connectors = []
        # todo: universal class contanier for system, chasis, etc could be done
        self.system = ControllerTools()
        self.systems_interfaces = {}
        self.chassis_interfaces = []
