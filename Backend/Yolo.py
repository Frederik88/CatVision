import numpy as np
import os
import time
import cv2

from Backend.BoundingBox import BoundingBox
from Backend.ObjectDetection import ObjectDetection


class Yolo(ObjectDetection):

    def __init__(self):
        """
        Creates a ObjectDetection object for the Yolo algorithm.
        Paths to the class, weight and cfg file are initialized
        in the constructor. The model is created from the initiated files.
        """
        ObjectDetection.__init__(self)
        print('[YOLO INIT] Initialize Yolo ')

        print('[YOLO INIT] Setting paths ')
        path = os.path.dirname(os.path.abspath(__file__))
        yolo_path = path + '\yolo'
        labels_path = yolo_path + '\obj.names'
        weights_path = yolo_path + '\yolov3.weights'
        config_path = yolo_path + '\yolov3.cfg'

        print('[YOLO INIT] Current dir: ', path)
        print('[YOLO INIT] Weights path: ', weights_path)
        print('[YOLO INIT] Config path: ', config_path)

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
        self.__class_labels = open(labels_path).read().strip().split('\n')
        self.__class_colors = [
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255]
        ]

        # Load Yolo detector from darknet
        print("[YOLO INIT] loading YOLO from disk...")
        self.__net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
        print("[YOLO INIT] loading YOLO finished...")

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
        conf variable. Overlapping bounding boxes are removed through nms-suppression.
        The remaining bounding boxes are drawn around their respective objects.
        The coordinates of the bounding boxes are checked for intersection.

        :param image: Input image
        :param conf: confidence threshold
        :param thresh: threshold for nms
        :param area: area of the intersection roi
        :return: image with drawn bounding boxes
        """
        (H, W) = image.shape[:2]

        # get output layer from net
        ln = self.__net.getLayerNames()
        ln = [ln[i[0] - 1] for i in self.__net.getUnconnectedOutLayers()]

        # create blob from image
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        self.__net.setInput(blob)
        start = time.time()
        layer_outputs = self.__net.forward(ln)
        end = time.time()

        # show timing information on YOLO
        print("[YOLO PASS] YOLO took {:.6f} seconds".format(end - start))

        # Variables to hold boxes, confidences and IDs
        boxes = []
        confidences = []
        class_ids = []

        # loop over each of the layer outputs
        for output in layer_outputs:
            # loop over each of the detections
            for detection in output:
                # Get IDs and confidences
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Apply filter for confidence to discard weak predictions
                if confidence > conf:
                    # get bounding box coordinates and scale back to size of the
                    # image
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # Append box, conf and ID to lists
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # To remove overlapping and weak bounding-boxes, apply NMS
        nms_idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf,
                                    thresh)

        # Check if at least one detection exists
        if len(nms_idxs) > 0:
            # loop over indices
            for i in nms_idxs.flatten():

                # Get coordinates of bbox
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # Add the nms bounding box to bbox array
                bbox = BoundingBox(x, y, w, h, class_ids[i], confidences[i])
                self.__bounding_boxes.append(bbox)

                idx = int(class_ids[i])

                # Draw bounding boxes with label and center dot
                color = [int(c) for c in self.__class_colors[idx]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                cv2.circle(image, bbox.calc_center(), 5, color, -1, 8)
                text = "{}: {:.4f}".format(self.__class_labels[idx], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

                # Check for ROI intersection
                x1 = 640 // 2
                x2 = 640 // 2
                y1 = 0
                y2 = 480
                bbox.check_intersect_with_roi(x1, x2, y1, y2, area)

                if bbox.get_counted_status():
                    print("Bbox get counted status: ",bbox.get_counted_status())
                    self.__detected_class = bbox.get_class_name()
                    self.__detected_conf = bbox.get_confidence()

                    if bbox.get_box_id() == 0:
                        self.__object_one = self.__object_one + 1

                    if bbox.get_box_id() == 1:
                        self.__object_two = self.__object_two + 1

                    if bbox.get_box_id() == 2:
                        self.__object_three = self.__object_three + 1

        return image
