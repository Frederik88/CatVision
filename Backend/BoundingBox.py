import numpy as np


class BoundingBox:

    def __init__(self, x, y, w, h, idx, conf):
        """

        Creates a bounding box of a detected object
        with their corresponding location, id and confidence.

        :param x: x-coordinate top left
        :param y: y-coordinate top left
        :param w: width of the bounding box
        :param h: height of the bounding box
        :param idx: id of the detected object
        :param conf: confidence of the detected object
        """
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__idx = idx
        self.__conf = conf
        self.__counted = False

    def calc_center(self):
        """
        Calculate the center position of the bounding box.

        :return: tuple of the x- and y-coordination of the center
        position
        """
        x = int(self.__x + self.__w/2)
        y = int(self.__y + self.__h/2)
        return x, y

    def get_confidence(self):
        return self.__conf

    def get_location(self):
        return self.__x, self.__y, self.__w, self.__h

    def set_box_id(self, idx):
        self.__idx = idx

    def get_box_id(self):
        return self.__idx

    def get_counted_status(self):
        return self.__counted

    def to_string(self):
        out_string = ("Position: "+str(self.__x)+" "+str(self.__y)+" "+str(self.__w)+" "+str(self.__h)+"\n"
                      "ID: "+str(self.__idx)+"\n"
                      "Counted: "+str(self.__counted)+"\n"
                      "Class name: "+self.get_class_name()+"\n")

        return out_string

    def check_intersect_with_roi(self, roi_x1, roi_x2, roi_y1, roi_y2, roi_range):
        """
        Checks if the bounding box objects intersects with the roi position.
        Returns true when intersecting and false if not intersection.

        :param roi_x1: top left x-coordinate
        :param roi_x2: top left y-coordinate
        :param roi_y1: bottom right x-coordinate
        :param roi_y2: bottom left y-coordinate
        :param roi_range: size of the roi
        :return: boolean status of intersection
        """
        if roi_x1 == roi_x2:
            roi_x1 == roi_x2

        if roi_y1 == roi_y2:
            roi_y1 == roi_y2

        if (
            self.calc_center()[0] > roi_x1 - roi_range and
            self.calc_center()[0] < roi_x1 + roi_range and
            self.calc_center()[1] > roi_y1 and
            self.calc_center()[1] < roi_y2
           ):
            self.__counted = True

    def get_class_name(self):
        """
        Returns the class name of the corresponding class id.

        :return: class name as string
        """
        class_name = ""

        if self.__idx == 0:
            class_name = "Hazelnut"

        if self.__idx == 1:
            class_name = "walnut"

        if self.__idx == 2:
            class_name = "peanut"

        return class_name

    def calc_euclid_distance(self, b_box):
        # Get center of self and b_box

        center_self = self.calc_center()
        center_bbox = b_box.calc_center()

        # Calc euclidean distance between the boxes
        euclid_distance = np.linalg.norm(np.asarray(center_self) - np.asarray(center_bbox))

        return euclid_distance






