import socket
from io import BytesIO
from time import sleep
import cv2
from picamera import PiCamera

class CameraControl:
    
    def __init__(self):
        """
        Creating object for camera control
        """
        #self.__camera = PiCamera()
        #self.__camera.resolution = (2560,1936)
        #self.__img = BytesIO()
        
    def start_capture(self):
        #self.__camera.start_preview()
        #print("[CAM CTRL] Start Capturing")
        #sleep(2)
        #self.__camera.capture(self.__img, 'jpeg')
        #self.__camera.stop_preview()
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            raise IOError('Cannot open webcam')
        
        frame = cap.read()[1]
        cap.release()
        
        return frame
        