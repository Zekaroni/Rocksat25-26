import os
from picamera2 import Picamera2

class RocketCamera:
    def __init__(self, runID: int):
        self._camera: Picamera2 = Picamera2()
        self._recording  = False
        self._duration   = 0 # Indefinite
        self._parent_folder = f"./data/{runID}"
        self.__ensure_folder_exists__()
        self._output_path = f"{self._parent_folder}/video.h264"
        self._width      = 1920
        self._height     = 1080
        self._fps        = 30

    def __ensure_folder_exists__(self):
        if not os.path.exists(self._parent_folder):
            os.mkdir(self._parent_folder)

    @property
    def recording(self):
        return self._recording

    # NOTE: Removed for less in-flight overhead
    # def setResolution(self, resolution: list|tuple[int,int]) -> bool:
    #     if type(resolution) not in [list, tuple]:
    #         raise TypeError("Invalid argument")
        
    #     if len(resolution) != 2:
    #         raise ValueError("Invalid list parameter")
        
    #     if resolution[0] > 4656:
    #         raise ValueError("Width value too large")
        
    #     if resolution[1] > 3496:
    #         raise ValueError("Height value too large")
        
    #     # NOTE: May not use this to avoid a possible exception during flight run 
    #     pass
    
    # def setFPS(self, newFPS) -> bool:
    #     pass

    def startRecording(self):
        self._camera.start_and_record_video(self._output_path)

    def stopRecording(self):
        self._camera.stop_recording()