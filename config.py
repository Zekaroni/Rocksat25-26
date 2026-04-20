class CameraConfig:
    # Decided not to use this for final product because of the
    # overhead it adds for possible issues
    WIDTH  = 1920
    HEIGHT = 1080
    FPS    = 30
    OUTPUT = ""

class SystemsPollingRates:
    # This is the amount of time a loop will sleep based on 1/x (Hz)
    # BNO055   = 200 # We want this uncapped and running as fast as possible
    MLX90393 = 20
    DS18B20  = 5
    PIZERO2W = 1

