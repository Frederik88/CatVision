import socket
from time import sleep
from picamera import PiCamera

class CameraControl:
    
    def __init__(self):
        """
        Creating object for camera control
        """
        self.__camera = PiCamera()
        self.__camera.resolution = (2560,1936)
        
    def start_capture(self):
        self.__camera.start_preview()
        sleep(5)
        print("[CAM CTRL] Start Capturing")
        self.__camera.capture('test.jpg')
        self.__camera.stop_preview()
        