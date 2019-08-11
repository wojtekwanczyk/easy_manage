
class Sensor:
    def __init__(self, ipmi):
        self.ipmi = ipmi

    def reading(self, sensor_number, lun=0):
        """Utility used to fetch reading from one specific sensor, with 0 LUN"""
        return self.ipmi.get_sensor_reading(sensor_number, lun)

    def mass_read(self, sensors):
        """
            Mass read for sensors list, assigns to self.reading new reading value
            TODO: Perhaps create own data structure for storing sensor objects

            :param: List of sensor objects
            :return: None
        """
        for sensor in sensors:
            sensor.reading = self.reading(sensor.number)

    # (Set/Get)SensorHysteresis
    # (Set/Get)SensorThresholds
    # (Set/Get)SensorEventEnable
    # GetDeviceSdrInfo
    # ReserveDeviceSdrRepository
    # GetDeviceSdr
    # RearmSensorEvents
