import logging
import cv2
import numpy as np

from .interface import CaptureSource, ObjectDetector
from .sim_pymunk import AirHockeyGame

MASK_WIN_NAME = 'HHR - Mask'

class NoVideoSourceError(Exception):
    pass

def detect_circular_object(frame, hsv_min, hsv_max, circle_color, draw_contours=False):
    # Make a copy of the original frame so we can modify it
    hsv_frame = frame.copy()

    # Convert from BGR to HSV then use ranges to seperate out the object we are interested in
    hsv_frame = cv2.cvtColor(hsv_frame, cv2.COLOR_BGR2HSV);
    mask = cv2.inRange(hsv_frame, hsv_min, hsv_max)

    # Try reduce amount speckles around the object we are detecting
    mask = cv2.medianBlur(mask, 7)

    # Find all contours in the mask
    # With debugging enabled draw all of them in red
    contours, hierarchy = cv2.findContours(mask.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    
    largest_cnt = None
    largest_area = -1 
    for cnt in contours:
        curr_area = cv2.contourArea(cnt)
        if curr_area > largest_area:
            largest_cnt = cnt

    # Convert mask back to color so we can draw on it
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    if draw_contours:
        cv2.drawContours(mask, contours, -1, (0,0,255), 3)

    # Find the circle bounding the contour with the largest area
    # The x, y of this circle should be the center of our object
    # With debugging enabled draw this circle in the passed color
    x, y, radius = -1, -1, -1
    try:
        if largest_cnt != None:
            (x, y), radius = cv2.minEnclosingCircle(largest_cnt)
            center = (int(x), int(y))
            radius = int(radius)

            cv2.circle(mask, center,radius, circle_color, 2)
    except cv2.error as exc:
        # Errors will also be displayed by the C++ part
        logging.error("Failure to find enclosing circle")

    return (x,y), radius, mask

class CV2CaptureSource(CaptureSource):
    def __init__(self, video_id, width, height):
        self.video_id = video_id
        self.cap = cv2.VideoCapture(video_id)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)

    def __del__(self):
        self.release()

    def frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise NoVideoSourceError("OpenCV could not access video source: %s" % self.video_id)
        return frame

    def release(self):
        self.cap.release()

class SimulatedCaptureSource(CaptureSource):
    def __init__(self, width, height):
        self.game = AirHockeyGame(width, height)

    def frame(self):
        self.game.process_frame()
        frame = self.game.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR);
        return frame

    def release(self):
        pass

class VisionDetector(ObjectDetector):
    def __init__(self, source, threshold):
        # Create window for threshold mask, not needed by
        # other detectors
        cv2.namedWindow(MASK_WIN_NAME, cv2.WINDOW_AUTOSIZE)

        self.source = source
        self.threshold = threshold

    def frame(self):
        return self.source.frame()

    def object_location(self):
        frame = self.frame()

        mask = np.zeros(frame.shape, np.uint8)
        if self.threshold != None and self.threshold.enabled():
            hsv_min = self.threshold.min_values()
            hsv_max = self.threshold.max_values()

            coords, radius, thresh_mask = detect_circular_object(frame, hsv_min, hsv_max, (255,0,0))
            mask = cv2.add(mask, thresh_mask)

            cv2.imshow(MASK_WIN_NAME, mask)

            return coords, radius
        else:
            return None
