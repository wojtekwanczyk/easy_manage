class Abstract:
    """Abstract class that all abstract interfaces must implement
    also they must  only implement methods that can be invoked by other classes(public methods)"""

    def __init__(self, abstract):
        "Abstract instances are used in controller_factory"
        self.abstract = abstract

    def get_methods(self):
        "Returns list of possible methods"
        if not self.abstract:
            return [method_name for method_name in dir(self) if
                    callable(getattr(self, method_name)) and not method_name.startswith('__')]
        else:
            return []
