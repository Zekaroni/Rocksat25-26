import adafruit_mlx90393

class MLX90393:
    def __init__(self, i2c_bus):
        self.sensor = adafruit_mlx90393.MLX90393(i2c_bus)
    
    @property
    def magnetic(self) -> tuple[float, float, float]:
        """
        Magnetic property for the MLX90393.
        Measured in microteslas and are signed floats
        
        :return: tuple(MX, MY, MZ)
        :rtype: Tuple
        """
        return self.sensor.magnetic