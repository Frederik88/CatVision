import time
import cv2
import sys
import types

sys.path.append('../')

from Backend.Yolo import Yolo
from Backend.FasterRCNN import FasterRCNN
from Backend.TinyYolo import TinyYolo
from Backend.SSD import SSD
from Backend.FrameShow import FrameShow


class Stream:

    def __init__(self):
        """
        Class for handling the image stream and processing of the application.
        The object detection algorithms are initialized here, as wells as the
        image stream from the ip camera. The constructor initializes parameters
        for time measurement and evaluation of the detection performance.
        """
        self.__fps = 0
        self.__seconds = 0
        self.__num_frames = 0
        self.__start_time = 0

        self.__counter_obj_one = 0
        self.__counter_obj_two = 0
        self.__counter_obj_three = 0

        self.__class_name = ""
        self.__class_confidence = 0

        self.__yolo = types.SimpleNamespace
        self.__ssd = types.SimpleNamespace
        self.__rcnn = types.SimpleNamespace
        self.__tiny_yolo = types.SimpleNamespace

        self.__frame_show = types.SimpleNamespace

    def load_net_parameters(self):
        """
        Initializes the object detection classes and
        their respective models.
        """
        self.__yolo = Yolo()
        self.__ssd = SSD()
        self.__rcnn = FasterRCNN()
        self.__tiny_yolo = TinyYolo()

    def __get_class_name(self):
        return self.__class_name

    def __get_class_conf(self):
        return self.__class_confidence

    def __get_fps(self):
        return self.__fps

    def __get_seconds(self):
        return round(self.__seconds, 2)

    def __get_obj1(self):
        return self.__counter_obj_one

    def __set_obj1(self, obj1):
        self.__counter_obj_one = obj1

    def __get_obj2(self):
        return self.__counter_obj_two

    def __set_obj2(self, obj2):
        self.__counter_obj_two = obj2

    def __get_obj3(self):
        return self.__counter_obj_three

    def __set_obj3(self, obj3):
        self.__counter_obj_three = obj3

    # Properties
    frames_per_second = property(__get_fps)
    ms_second = property(__get_seconds)

    class_name = property(__get_class_name)
    class_conf = property(__get_class_conf)

    obj1 = property(__get_obj1, __set_obj1)
    obj2 = property(__get_obj2, __set_obj2)
    obj3 = property(__get_obj3, __set_obj3)

    def fetch_frame_data(self):
        """
        Initializes the image stream from the ip
        camera and starts the stream. Returns a
        FrameShow object for accessing the image data.

        :return FrameShow object
        """
        self.__frame_show = FrameShow()
        self.__frame_show.start()
        self.__start_time = time.time()

        return self.__frame_show


    def start_processing(self, image, check_yolo, check_tiny_yolo, check_rcnn, check_ssd):
        """
        Method for handling the image data processing. Depending on the chose object detection
        algorithm, image data gets processed with one of the four algorithms. For performance
        measurement, the fps and milliseconds of the processing time are measured and displayed
        in the returned image. To count a detected object, a roi line is displayed in the middle
        of the image. The object detection algorithms are performing a check, if a detected object
        intersects the roi line.

        :param image: input image data
        :param check_yolo: boolean value if yolo should be used for detection
        :param check_tiny_yolo: boolean value if tiny yolo should be used for detection
        :param check_rcnn: boolean value if faster r-cnn should be used for detection
        :param check_ssd: boolean value if ssd should be used for detection
        :return: processed image with drawn performance values and roi line.
        """
        self.__num_frames = self.__num_frames + 1
        overlay = image.copy()
        area = 2
        if check_yolo:
            try:
                area = 15
                self.__yolo.forward_pass(image, 0.5, 0.3, area)
                [self.__counter_obj_one, self.__counter_obj_two, self.__counter_obj_three,
                 self.__class_name, self.__class_confidence] \
                    = self.__yolo.fetch_detected_objects()
            except:
                print('YOLO Net Parameter not loaded')

        if check_tiny_yolo:
            try:
                area = 15
                self.__tiny_yolo.forward_pass(image, 0.5, 0.3, area)
                [self.__counter_obj_one, self.__counter_obj_two, self.__counter_obj_three,
                 self.__class_name, self.__class_confidence] \
                    = self.__tiny_yolo.fetch_detected_objects()
            except:
                print('TINY YOLO Net Parameter not loaded')

        if check_rcnn:
            try:
                area = 15
                self.__rcnn.forward_pass(image, 0.5, 0.3, area)
                [self.__counter_obj_one, self.__counter_obj_two, self.__counter_obj_three,
                 self.__class_name, self.__class_confidence]\
                    = self.__rcnn.fetch_detected_objects()
            except:
                print('FASTER R-CNN Net Parameter not loaded')

        if check_ssd:
            try:
                area = 15
                self.__ssd.forward_pass(image, 0.5, 0.3, area)
                [self.__counter_obj_one, self.__counter_obj_two, self.__counter_obj_three,
                 self.__class_name, self.__class_confidence]\
                    = self.__ssd.fetch_detected_objects()
            except:
                print('SSD Net Parameter not loaded')

        end_time = time.time()
        self.__seconds = (end_time - self.__start_time)  # * 10**3

        # Printing ms to image
        cv2.putText(image, str("%.2f seconds" % round(self.__seconds, 2)), (400, 450), cv2.FONT_HERSHEY_SIMPLEX
                    , 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Printing fps to image
        cv2.putText(image, str("FPS: %.0f" % self.__fps), (30, 450), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2, cv2.LINE_AA)

        x1 = 640 // 2
        x2 = 640 // 2
        y1 = 0
        y2 = 480

        # Draw ROI line for tracking
        cv2.line(overlay, (x1, y1), (x2, y2), (0, 255, 0), area)
        alpha = 0.4
        image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

        image = cv2.imencode('.jpg', image)[1].tobytes()

        if self.__seconds >= 1:
            self.__fps = self.__num_frames
            self.__num_frames = 0
            self.__start_time = time.time()

        return image
