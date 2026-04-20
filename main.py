from lib.SC_BNO055 import BNO055
from lib.SC_CAMERA import RocketCamera
from lib.SC_DS18B20 import DS18B20
from lib.SC_LOGGING import DataLog, BNOLogger
from lib.SC_MLX90393 import MLX90393
from lib.SC_PIZERO2W import PiZeroBoard

from config import SystemsPollingRates

import os
import board
import threading
import time

def getRunID():
    return len(os.walk("./data")[1]) + 1

def bno_loop(runID, i2c):
    bno055 = BNO055(i2c)
    logger = BNOLogger(runID)
    last_buffer = bytearray(26)
    while True:
        ts = time.monotonic_ns()
        current_buffer = bno055.get_raw_bytes()
        if current_buffer != last_buffer:
            logger.logRawBytes(ts, current_buffer)
            last_buffer[:] = current_buffer

def mlx_loop(runID, i2c):
    mlx90393 = MLX90393(i2c)
    logger = DataLog(runID, "mlx90393") 
    while True:
        logger.write(f"{time.time()},{mlx90393.magnetic}")
        time.sleep(1/SystemsPollingRates.MLX90393) 

def temp_loop(runID):
    ds18b20 = DS18B20()
    logger = DataLog(runID, "ds18b20")
    while True:
        logger.write(f"{time.time()},{ds18b20.temperature}")
        time.sleep(1/SystemsPollingRates.DS18B20)

def sys_loop(runID):
    piZero = PiZeroBoard()
    logger = DataLog(runID, "system")
    while True:
        logger.write(f"{time.time()},{piZero.CPUTemperature},{piZero.CPULoad},{piZero.MEMUsage}")
        time.sleep(1/SystemsPollingRates.PIZERO2W) 

if __name__ == "__main__":
    runID = getRunID()

    i2c = board.I2C()
    
    # Init the camera and start recording
    # TODO: Add debug LED
    cam = RocketCamera(runID)
    cam.startRecording()
    
    threading.Thread(target=bno_loop, args=(runID, i2c), daemon=True).start()
    threading.Thread(target=mlx_loop, args=(runID, i2c), daemon=True).start()
    threading.Thread(target=temp_loop, args=(runID), daemon=True).start()
    threading.Thread(target=sys_loop, args=(runID), daemon=True).start()
    
    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        cam.stopRecording()