"Controller "


class ControllerTools:
    """Abstract class that all abstract interfaces must implement
    also they must  only implement methods that can be invoked by other classes(public methods)"""

    def get_methods(self):
        "Returns list of possible methods"
        return [method_name for method_name in dir(self) if
                callable(getattr(self, method_name)) and not method_name.startswith(
                    '_') and method_name != 'assign_missing_methods']

    def assign_missing_methods(self, donor):
        "Reassigns available methods call from donor to recipient"
        new_methods = list(set(donor.get_methods()) - set(self.get_methods()))
        for method in new_methods:
            setattr(self, method, getattr(donor, method))
