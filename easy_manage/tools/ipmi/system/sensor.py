"Module for sensor-specific operations"


class Sensor:
    "Class which is for reading sensor's values and converting it to proper formats"

    def __init__(self, ipmi):
        self.ipmi = ipmi

    def sensor_reading(self, sdr):
        """Utility used to fetch reading from one specific sensor, based on it's SDR"""
        raw_reading = self.ipmi.get_sensor_reading(sdr.number, sdr.lun)
        return sdr.parse_reading(raw_reading)

    def mass_read_sensor(self, sdr_list):
        """
            Mass read for sensors list, assigns to self.reading new reading value
            :param sdr_list: List of SDR objects whose values need to be fetched
            :return: Dict with <key>:<value> => <sensor_number>:<sensor_reading>
        """
        readings = {}
        for sdr in sdr_list:
            readings[sdr.name] = self.sensor_reading(sdr)
            return readings
