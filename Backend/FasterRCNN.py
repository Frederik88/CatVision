import numpy as np
import os
import time
import cv2


from Backend.BoundingBox import BoundingBox
from Backend.ObjectDetection import ObjectDetection


class FasterRCNN(ObjectDetection):

    def __init__(self):
        """
        Creates a ObjectDetection object for the Faster R-CNN algorithm.
        Paths to the class, inference and prototext file are initialized
        in the constructor. The model is created from the initiated files.
        """
        ObjectDetection.__init__(self)
        print('[FASTERRCNN INIT] Initialize FasterRCNN ')

        print('[FASTERRCNN INIT] Setting paths ')
        path = os.path.dirname(os.path.abspath(__file__))
        faster_rcnn_path = path + '\\fasterrcnn'
        class_path = faster_rcnn_path + '\classes.txt'
        frozen_inference = faster_rcnn_path + '\\frozen_inference_graph.pb'
        graph_proto = faster_rcnn_path + '\graph.pbtxt'

        print('[FASTERRCNN INIT] Current dir: ', path)
        print('[FASTERRCNN INIT] Frozen Inference path: ', frozen_inference)
        print('[FASTERRCNN INIT] Graph Proto path: ', graph_proto)

        # Init vars for tracking
        self.__bounding_boxes = []

        # Counter for detected objects
        self.__object_one = 0
        self.__object_two = 0
        self.__object_three = 0

        self.__detected_class = ""
        self.__detected_conf = 0

        # List of colors for each object class
        # Hazelnut = red
        # Walnut = blue
        # Peanut = green
        self.__class_labels = open(class_path).read().strip().split('\n')
        self.__class_colors = [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255]
        ]

        # Load faster r-cnn inference graph
        print("[FASTERRCNN INIT] loading FasterRCNN from disk...")
        self.__net = cv2.dnn.readNetFromTensorflow(frozen_inference, graph_proto)
        print("[FASTERRCNN INIT] loading FasterRCNN finished...")

    def fetch_detected_objects(self):
        """
        Returns a tuple containing the counters for detected objects,
        the class of the current detected object and its confidence

        :return: Tuple of obj1, obj2, obj3, class name and confidence
        """
        return self.__object_one, \
               self.__object_two, \
               self.__object_three, \
               self.__detected_class, \
               self.__detected_conf

    def forward_pass(self, image, conf, thresh, area):
        """
        Performs a forward pass through the net of the chosen object detection
        algorithm. A blob gets created from the input image and gets passed
        through the net. The output of the net is an array containing the
        coordinates of the created bounding boxes, their class ids and confidences.
        Weak detections get discarded when the confidence is lower than the value of the
        conf variable. The remaining bounding boxes are drawn around their respective objects.
        The coordinates of the bounding boxes are checked for intersection.

        :param image: Input image
        :param conf: confidence threshold
        :param thresh: threshold for nms (not used)
        :param area: area of the intersection roi
        :return: image with drawn bounding boxes
        """

        H, W, channels = image.shape

        blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)
        self.__net.setInput(blob)
        start = time.time()
        layer_outputs = self.__net.forward()
        end = time.time()

        # show timing information on FasterRCNN
        print("[FASTERRCNN PASS] FasterRCNN took {:.6f} seconds".format(end - start))

        # Loop through output, drawing bounding boxes from output
        for detection in layer_outputs[0, 0]:

            confidence = float(detection[2])
            if confidence > conf:
                # Get coordinate of bbox
                x1 = int(detection[3] * W)
                y1 = int(detection[4] * H)
                x2 = int(detection[5] * W)
                y2 = int(detection[6] * H)

                class_id = int(detection[1])

                # Add the bounding box to bbox array
                bbox = BoundingBox(x1, y1, (x2-x1), (y2-y1), class_id, confidence)
                self.__bounding_boxes.append(bbox)

                # Draw bounding boxes with label and center dot
                color = [int(c) for c in self.__class_colors[class_id]]
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.circle(image, bbox.calc_center(), 5, color, -1, 8)
                text = "{}: {:.4f}".format(self.__class_labels[class_id], confidence)
                cv2.putText(image, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

                # Check for ROI intersection
                x1 = 640 // 2
                x2 = 640 // 2
                y1 = 0
                y2 = 480
                bbox.check_intersect_with_roi(x1, x2, y1, y2, area)

                if bbox.get_counted_status():

                    self.__detected_class = bbox.get_class_name()
                    self.__detected_conf = bbox.get_confidence()

                    if bbox.get_box_id() == 0:
                        self.__object_one = self.__object_one + 1
                    if bbox.get_box_id() == 1:
                        self.__object_two = self.__object_two + 1
                    if bbox.get_box_id() == 2:
                        self.__object_three = self.__object_three + 1

        return image
