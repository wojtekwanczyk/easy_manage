from easy_manage.tools.ipmi.chassis.chassis_messages import ChassisControl 

class IpmiChassisTools: 
    def __init__(self, ipmi):
        self.ipmi = ipmi
        
    def functions(self):
        # TODO: Test this 
        return self.ipmi.send_message_with_name('GetChassisCapabilities')
    
    def status(self):
        # TODO: Check return object
        return self.ipmi.get_chassis_status()
        
    def __set_chassis_power(self,power_status):
        self.ipmi.chassis_control(power_status)
    
    def power_up(self):
        self.__set_chassis_power(ChassisControl.POWER_UP)
        
    def power_cycle(self):
        self.__set_chassis_power(ChassisControl.POWER_CYCLE)

    def power_down(self):
        self.__set_chassis_power(ChassisControl.POWER_DOWN)
        
    def hard_reset(self):
        self.__set_chassis_power(ChassisControl.HARD_RESET)
        
    def diagnostic_interrupt(self):
        self.__set_chassis_power(ChassisControl.DIAGNOSTIC_INTERRUPT)
        
    def soft_shutdown(self):
        self.__set_chassis_power(ChassisControl.SOFT_SHUTDOWN)
    
    # TODO: Check if it's possible to implement this    
    #def blink_led(self):
    #    pass
        
    def power_on_hours(self):
        return self.ipmi.send_message_with_name('GetPohCounter')