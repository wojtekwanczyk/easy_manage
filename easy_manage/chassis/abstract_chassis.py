class AbstractChassis():
    def __init__(self, system_name, connector):
        self.system_name = system_name
        self.connector = connector
        self.db = connector.db
        self.data = {}
        self.last_update = None