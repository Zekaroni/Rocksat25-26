import threading
from gpiozero import LED

class StatusLED:
    def __init__(self, pin=17):
        self.led: LED = LED(pin)
        self.is_error = False
        self._lock = threading.Lock()

    def system_ready(self):
        with self._lock:
            if not self.is_error:
                self.led.on()

    def standby(self):
        with self._lock:
            if not self.is_error:
                self.led.blink(on_time=0.5, off_time=0.5)

    def trigger_error(self):
        with self._lock:
            if not self.is_error:
                self.is_error = True
                self.led.blink(on_time=0.05, off_time=0.05)