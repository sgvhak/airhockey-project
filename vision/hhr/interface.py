from abc import ABCMeta, abstractmethod

## GUI Stuff ##
class HSVThreshold(object):
    'Represents a container with set of min and max HSV values.'

    __metaclass__ = ABCMeta

    @abstractmethod
    def min_values(self):
        'Returns a numpy array with the 3 HSV minimum values'
        return

    @abstractmethod
    def max_values(self):
        'Returns a numpy array with the 3 HSV maximum values'
        return

    @abstractmethod
    def enabled(self):
        'Return true if this threshold is enabled'
        return

class CaptureSource(object):
    'Represents a source of frame data for the vision subsystem.'

    __metaclass__ = ABCMeta

    @abstractmethod
    def frame(self):
        'Returns a frame of video in CV2 RGB color space as a numpy array'
        return

    @abstractmethod
    def release(self):
        'Release any objects that need cleanup'
        return

class PuckPredictor(object):
    'Represents a class that accepts puck events and builds a prediction of where it will be'

    __metaclass__ = ABCMeta

    @abstractmethod
    def threshold(self):
        'Return the HSVThreshold object associated with the predictor'

        return

    @abstractmethod
    def add_puck_event(self, tick, coords, radius):
        'Adds an event where the puck was last seen'

        return

    @abstractmethod
    def intercept_point(self):
        'Returns the location the paddle should go to intercept the puck'

        return

    @abstractmethod
    def draw(self, frame):
        'Draws prediction values and simulation bounds on an OpenCV frame'

        return

class RobotController(object):
    'Uses predicted paths to control some part of the robot'

    __metaclass__ = ABCMeta

    @abstractmethod
    def move_to(self, intercept_point):
        'Move paddle to interception point'

        return

