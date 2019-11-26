"It contains only Controller instance"


class Controller(dict):
    "It's responsible for controlling whole server functionality"
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, *kwargs)

        self.standards = {}
        self.components = {}
        self['system'] = type('', (), {})()
        self['chassis'] = type('', (), {})()
        self['shell'] = type('', (), {})()
