import numpy as np
import os
import time
import cv2
import tensorflow as tf


from Backend.BoundingBox import BoundingBox
from Backend.ObjectDetection import ObjectDetection


class SSD(ObjectDetection):

    def __init__(self):
        """
        Creates a ObjectDetection object for the SSD algorithm.
        Paths to the class, weight and cfg file are initialized
        in the constructor. The model is created from the initiated files.
        """
        ObjectDetection.__init__(self)
        print('[SSD INIT] Initialize SSD ')

        print('[SSD INIT] Setting paths ')
        path = os.path.dirname(os.path.abspath(__file__))
        ssd_path = path + '\ssd'
        class_path = ssd_path + '\classes.txt'
        frozen_inference = ssd_path + '\\frozen_inference_graph.pb'

        print('[SSD INIT] Current dir: ', path)
        print('[SSD INIT] Frozen Inference path: ', frozen_inference)

        # Init vars for tracking
        self.__bounding_boxes = []

        # Counter for detected objects
        self.__object_one = 0
        self.__object_two = 0
        self.__object_three = 0

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

        # Read the graph.
        with tf.gfile.FastGFile(frozen_inference, 'rb') as f:
            self.__net = tf.GraphDef()
            self.__net.ParseFromString(f.read())

        self.__session = tf.Session()
        self.__session.graph.as_default()
        tf.import_graph_def(self.__net, name='')

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
        conf variable. The remaining bounding boxes are drawn around their respective
        objects. The coordinates of the bounding boxes are checked for intersection.

        :param image: Input image
        :param conf: confidence threshold
        :param thresh: threshold for nms
        :param area: area of the intersection roi
        :return: image with drawn bounding boxes
        """

        # Read and preprocess an image.
        img = image
        rows = img.shape[0]
        cols = img.shape[1]
        inp = cv2.resize(img, (300, 300))
        inp = img[:, :, [2, 1, 0]]  # BGR2RGB

        # Run the model
        out = self.__session.run([self.__session.graph.get_tensor_by_name('num_detections:0'),
                                self.__session.graph.get_tensor_by_name('detection_scores:0'),
                                self.__session.graph.get_tensor_by_name('detection_boxes:0'),
                                self.__session.graph.get_tensor_by_name('detection_classes:0')],
                                feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

        # Visualize detected bounding boxes.
        num_detections = int(out[0][0])
        for i in range(num_detections):
            class_id = int(out[3][0][i]-1)
            confidence = float(out[1][0][i])
            bbox = [float(v) for v in out[2][0][i]]
            if confidence > conf:
                x1 = int(bbox[1] * cols)
                y1 = int(bbox[0] * rows)
                x2 = int(bbox[3] * cols)
                y2 = int(bbox[2] * rows)

                # Add the bounding box to bbox array
                bbox = BoundingBox(x1, y1, (x2-x1), (y2-y1), class_id, confidence)
                self.__bounding_boxes.append(bbox)

                # Draw bounding boxes with label and center dot
                color = [int(c) for c in self.__class_colors[class_id]]
                cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                cv2.circle(image, bbox.calc_center(), 5, color, -1, 8)
                text = "{}: {:.4f}".format(self.__class_labels[class_id], confidence)
                cv2.putText(image, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

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

        return img
