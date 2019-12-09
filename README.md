# easy-manage :fish:

This python package has been created to facilitate remote server management. 
It is focused on out-of-band management through IPMI and Redefish standards, however, 
it is possible to perform in-band management with it.

The reason of creation of such package is need to unify server management regardless of
standard or protocol we use below. Easy-manage delivers unified management interface. 


Easy-manage is able to connet either Network Interface Card assigned to BMC or whole system.
You can give multiple IP addresses to ControllerFactory and it will try to connect to all of them.
Example config:

```
from tools import Protocol
from utils import Credentials

bmc_credentials = Credentials('username', 'password')
system_credentials = Credentials('username2', 'password2')

config = {
    Protocol.REDFISH: {
        'address': bmc_ip_address,
        'credentials': bmc_credentials
    },
    Protocol.IPMI: {
        'address': bmc_ip_address,
        'credentials': bmc_credentials
    },
    Protocol.BASH: {
        'address': system_ip_address,
        'credentials': system_credentials
    },
}
```

Above configuration will enable user to connect to device with all three accessible protocols. 
To create abstract controller over theses interfaces, we need to use ControllerFactory

```
controller = ControllerFactory.get_controller(config)
```

Now it is ready to use.

```
# See all available system methods
print(ControllerFactory.get_methods(controller.system))

# See all available chassis methods
print(ControllerFactory.get_methods(controller.chassis))

# Test simple abstract methods
print(controller.get_power_state())
print(controller.get_led_state())
controller.power_on()
```

Connector depending on its configuration is able to aggregate up to three components:
 - System
 - Chassis
 - Shell

You can get bulk data from every component using pre-defined methods `redings()`, `static_data()` and `raw_data()` on controller components.

```
from pprint import pprint as pp

pp.print(controller.shell.readings())
pp.print(controller.system.statuc_data())
pp.print(controller.chassis.raw_data())
```

See more examples in demo/demo.py

Package has been designed to provide command line tool but it has not been binded with implemented functionalities yet.

Please note that this package came into existence as a part of bachelor's thesis and has not 
been commercially used and thus may be buggy.
