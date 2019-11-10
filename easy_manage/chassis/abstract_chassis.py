"Module which describes abstract chassis class"


class AbstractChassis():
    "Abstract chasiss class, for aggregating and unifying chassis functionalities"

    def __init__(self, connector):
        self.connector = connector
        self.data = {}
        self.last_update = None

    def get_power_state(self):
        pass

    def get_health(self):
        pass
