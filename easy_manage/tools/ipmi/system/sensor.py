"Module for sensor-specific operations"


class Sensor:
    "Class which is for reading sensor's values and converting it to proper formats"

    def __init__(self, ipmi):
        self.ipmi = ipmi

    def read_sensor(self, sensor_number, lun=0):
        """Utility used to fetch reading from one specific sensor, with 0 LUN"""
        return self.ipmi.get_sensor_reading(sensor_number, lun)

    def mass_read_sensor(self, sensors_list):
        """
            Mass read for sensors list, assigns to self.reading new reading value
            TODO: Perhaps create own data structure for storing sensor objects

            :param: List of sensor objects
            :return: Dict with <key>:<value> => <sensor_number>:<sensor_reading>
        """
        readings = {}
        for sensor_number in sensors_list:
            readings[sensor_number] = self.read_sensor(sensor_number)
