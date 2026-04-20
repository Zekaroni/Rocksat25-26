import adafruit_bno055

class BNO055:
    def __init__(self, i2c_bus):
        self.sensor = adafruit_bno055.BNO055_I2C(i2c_bus)

        # 0x14 is the starting register for Gyro data
        self.register_address = bytearray([0x14])
        
        # Pre-allocate 26 bytes (6 Gyro + 6 Euler + 8 Quat + 6 LinAccel)
        self.buffer = bytearray(26)
    
    def get_raw_bytes(self) -> bytearray:
        """Reads 14 bytes directly from the I2C registers."""
        with self.sensor.i2c_device as i2c:
            i2c.write_then_readinto(self.register_address, self.buffer)
        return self.buffer