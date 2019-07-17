
class Sensor:
    def __init__(self, ipmi):
        self.ipmi = ipmi

    # (Set/Get)SensorHysteresis
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
            try:
                sensor.reading = self.reading(sensor.number)
            except Exception as ex:
                print("EXCEPTION!!!!!1" + ex)

        # (Set/Get)SensorThresholds

    # (Set/Get)SensorEventEnable
        # GetDeviceSdrInfo
    # ReserveDeviceSdrRepository
    # GetDeviceSdr

    # GetSensorReading

    # RearmSensorEvents
