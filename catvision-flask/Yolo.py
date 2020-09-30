import numpy as np
import os
import time
import cv2

from ObjectDetection import ObjectDetection


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
        labels_path = yolo_path + '\coco.names'
        weights_path = yolo_path + '\yolov3-spp.weights'
        config_path = yolo_path + '\yolov3-spp.cfg'

        print('[YOLO INIT] Current dir: ', path)
        print('[YOLO INIT] Weights path: ', weights_path)
        print('[YOLO INIT] Config path: ', config_path)

        # List of colors for each object class
        # Hazelnut = red
        # Walnut = blue
        # Peanut = green
        self.__class_labels = open(labels_path).read().strip().split('\n')
        self.__confidence = 0
        self.__label = ""
        self.__class_colors = [
            [0, 0, 255]
        ]

        # Load Yolo detector from darknet
        print("[YOLO INIT] loading YOLO from disk...")
        self.__net = cv2.dnn.readNet(config_path, weights_path)
        print("[YOLO INIT] loading YOLO finished...")

    def forward_pass(self, image, conf, thresh):
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
        self.__confidence = 0
        self.__label = ""

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
                    (center_x, center_y, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))

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

                idx = int(class_ids[i])
                self.__confidence = confidences[i]
                self.__label = self.__class_labels[idx]
                
                # Draw bounding boxes with label
                color = [int(c) for c in self.__class_colors[0]]
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(self.__class_labels[idx], confidences[i])
                cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)
        
        return image, self.__label, self.__confidence
