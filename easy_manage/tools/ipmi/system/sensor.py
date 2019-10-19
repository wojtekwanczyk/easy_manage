"Module for sensor-specific operations"
import logging
log = logging.getLogger(__name__)


class Sensor:
    "Class which is for reading sensor's values and converting it to proper formats"

    def __init__(self, ipmi):
        self._ipmi = ipmi

    def read_sensor(self, sdr):
        """Utility used to fetch reading from one specific sensor, based on its SDR"""
        sensor_nr = sdr.record_key['sensor_number']
        lun = sdr.record_key['fru_owner_lun']
        raw_reading = self._ipmi.get_sensor_reading(sensor_nr, lun)
        return sdr.parse_sensor_reading(raw_reading)

    def mass_read_sensor(self, sdr_list):
        """
            Mass read for sensors list, assigns to self.reading new reading value
            :param sdr_list: List of SDR objects whose values need to be fetched
            :return: Dict with <key>:<value> => <sensor_number>:<sensor_reading>
        """
        readings = {}
        for sdr in sdr_list:
            readings[sdr.name] = {
                'reading': self.read_sensor(sdr),
                'unit': sdr.sensor_unit
            }
        return readings
