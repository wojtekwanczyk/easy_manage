

class Controller:

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.standards = []
        self.systems = []
        self.chassis = []
    
    def get_power_state(self):
        print(f"SYSTEMS: {self.systems}")
        return self.systems[0].get_power_state()
