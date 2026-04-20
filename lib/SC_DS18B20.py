from w1thermsensor import W1ThermSensor

class DS18B20:
    def __init__(self):
        self.sensor: W1ThermSensor = W1ThermSensor()

    @property
    def temperature(self) -> float:
        """
        Returns the temperature in Celsius.
        
        :return: Temperature in C
        :rtype: float
        """
        return self.sensor.get_temperature()