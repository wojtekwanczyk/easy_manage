"Module for sensor-specific operations"


class Sensor:
    "Class which is for reading sensor's values and converting it to proper formats"

    def __init__(self, ipmi):
        self.ipmi = ipmi

    def read_sensor(self, sensor_number, sdr, lun=0):
        """Utility used to fetch reading from one specific sensor, with 0 LUN"""
        raw_reading = self.ipmi.get_sensor_reading(sensor_number, lun)
        return sdr.parse_reading(raw_reading)

    def mass_read_sensor(self, sensor_nr_list, sdr_list):
        """
            Mass read for sensors list, assigns to self.reading new reading value

            :param sensor_nr_list: List of sensor numbers
            :param sdr_list: List of SDR objects
            :return: Dict with <key>:<value> => <sensor_number>:<sensor_reading>
        """
        readings = {}
        for sensor_number in sensor_nr_list:
            try:
                # TODO: Is sensor number sufficient param to identify a sensor?
                def is_owner_sdr(sdr): return sdr.number == sensor_number
                sdr = list(filter(is_owner_sdr, sdr_list))[0]
                readings[sensor_number] = self.read_sensor(
                    sensor_number, sdr, sdr.lun)

            except IndexError:
                # TODO: Add logging utility here
                print("SDR with this number was not found: " + str(sensor_number))
            return readings
