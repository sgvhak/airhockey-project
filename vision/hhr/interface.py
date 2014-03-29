from abc import ABCMeta, abstractmethod

## GUI Stuff ##
class HSVThreshold(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def min_values(self):
        "Returns a numpy array with the 3 HSV minimum values"
        return

    @abstractmethod
    def max_values(self):
        "Returns a numpy array with the 3 HSV maximum values"
        return

    @abstractmethod
    def enabled(self):
        "Return true if this threshold is enabled"
        return

class CaptureSource(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def frame(self):
        "Returns a frame of video in CV2 RGB color space as a numpy array"
        return

    @abstractmethod
    def release(self):
        "Release any objects that need cleanup"
        return
