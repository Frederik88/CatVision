from abc import ABC, abstractmethod


class ObjectDetection(ABC):
    """
    Abstract class for the object detection algorithms.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def forward_pass(self, image, conf, thresh):
        pass
