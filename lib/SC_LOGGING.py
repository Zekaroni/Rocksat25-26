import os
import time
import struct

from io import TextIOWrapper, BufferedWriter # Only for code editor

class DataLog:
    def __init__(self, runID: int, prefix: str = ""):
        self.prefix = prefix
        self._parent_folder = f"./data/{runID}"
        self.__ensure_folder_exists__()

        self._logFile: TextIOWrapper = open(f"{self._parent_folder}/{prefix}.csv")
        self._last_sync = time.time()
        self.open()

    def __ensure_folder_exists__(self):
        if not os.path.exists(self._parent_folder):
            os.mkdir(self._parent_folder)

    def open(self, logTime=True) -> str:
        self._logFile = self.__get_next_file__()
        if logTime:
            self._logFile.write(str(time.time()) + "\n")
            self._logFile.flush()
            os.fsync(self._logFile.fileno())
        self._last_sync = time.time()
        return self._logFile.name
    
    def write(self, data: str):
        self._logFile.write(data + "\n")
        
        current_time = time.time()
        if current_time - self._last_sync >= 1.0:
            self._logFile.flush()
            os.fsync(self._logFile.fileno())
            self._last_sync = current_time

    def close(self):
        if self._logFile:
            self._logFile.flush()
            os.fsync(self._logFile.fileno())
            self._logFile.close()

class BNOLogger:
    def __init__(self, runID: int):
        self._parent_folder = f"./data/{runID}"
        self.__ensure_folder_exists__()

        self.file: BufferedWriter = open(f"{self._parent_folder}/bno055.bin", "wb")
        self.last_sync = time.time()
        
        self._pack_timestamp = struct.Struct("<Q").pack
        self._write = self.file.write
        self._flush = self.file.flush
        self._fsync = os.fsync
        self._fileno = self.file.fileno()

    def __ensure_folder_exists__(self):
        os.makedirs(self._parent_folder, exist_ok=True)

    def logRawBytes(self, timestamp_ns: int, raw_sensor_bytes: bytearray):
        self._write(self._pack_timestamp(timestamp_ns) + raw_sensor_bytes)
        
        current_time = time.time()
        if current_time - self.last_sync >= 1.0:
            self._flush()
            self._fsync(self._fileno)
            self.last_sync = current_time

    def close(self):
        self._flush()
        self._fsync(self._fileno)
        self.file.close()