import psutil
import shutil

class PiZeroBoard:
    def __init__(self):
        pass

    @property
    def CPUTemperature(self) -> float:
        """
        Returns CPU temperature in centigrade
        
        :return: CPU temp in C
        :rtype: float
        """
        # Replace os.system call to avoid unnessecary overhead
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as tempFile:
            return float(tempFile.read().strip()) / 1000.0

    @property
    def CPULoad(self) -> float:
        """
        Returns the amount of stress on the CPU in a percentage
        
        :return: CPU usage %
        :rtype: float
        """
        return psutil.cpu_percent()

    @property
    def MEMUsage(self) -> float:
        """
        Returns percentage of memory in use

        :return: percentage of memory in use
        :rtype: float
        """
        return psutil.virtual_memory().percent

    @property
    def DiskUsage(self) -> int:
        """
        Returns the amount of bytes left on the drive
        
        :return: number of bytes left on drive
        :rtype: int
        """
        return shutil.disk_usage("/")[2]