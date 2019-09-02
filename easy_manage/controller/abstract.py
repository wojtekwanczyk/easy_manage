"Abstract module"


class Abstract:
    """Abstract class that all abstract interfaces must implement
    also they must  only implement methods that can be invoked by other classes(public methods)"""

    def __init__(self, abstract=False):
        "Abstract flag is used to determine if methods are implemented, it's usede in controller factory"
        self.abstract = abstract

    def get_methods(self):
        "Returns list of possible methods"
        if not self.abstract:
            return [method_name for method_name in dir(self) if
                    callable(getattr(self, method_name)) and not method_name.startswith(
                        '_') and method_name != 'assign_missing_methods']
        return []

    def assign_missing_methods(self, donor):
        "Reassigns available methods call from donor to recipient"
        if self.abstract:
            new_methods = donor.get_methods()
            self.abstract = False
        else:
            new_methods = list(set(donor.get_methods()) - set(self.get_methods()))
        for method in new_methods:
            setattr(self, method, getattr(donor, method))
