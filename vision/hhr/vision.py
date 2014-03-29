import logging
import cv2
import numpy as np

from .interface import CaptureSource
from .sim import AirHockeyTable, AirHockeyGame
from .gui import VID_WIN_NAME, OUT_WIN_NAME

# How many time values to save for averaging for calculating FPS
NUM_TIME_RECORDS = 5

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

    def frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("OpenCV could not access video source: %s" % self.video_id)
        return frame

    def release(self):
        self.cap.release()

class SimulatedCaptureSource(CaptureSource):
    def __init__(self, width, height):
        self.sim = AirHockeyGame(width, height)

    def frame(self):
        self.sim.process_frame()
        frame = self.sim.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR);
        return frame

    def release(self):
        pass

class Vision(object):
    def __init__(self, source, thresholds):
        self.thresholds = thresholds
        self.source = source

    def capture_loop(self):
        time_records = np.zeros(NUM_TIME_RECORDS, float)
        time_rec_idx = 0
        time_total = 0
        while(True):
            time_beg = cv2.getTickCount()

            # Capture frame-by-frame
            frame = self.source.frame()

            mask = np.zeros(frame.shape, np.uint8)
            for thresh in self.thresholds:
                if thresh.enabled():
                    hsv_min = thresh.min_values()
                    hsv_max = thresh.max_values()

                    coords1, radius, thresh_mask = detect_circular_object(frame, hsv_min, hsv_max, (255,0,0))
                    mask = cv2.add(mask, thresh_mask)

            time_end = (cv2.getTickCount() - time_beg) / cv2.getTickFrequency()

            # Record time value in a rolling sum where the oldest falls off
            # This way we can smooth out the FPS value
            oldest_val = time_records[time_rec_idx]
            if oldest_val > 0:
                time_total -= oldest_val 
            time_total += time_end 
            time_records[time_rec_idx] = time_end
            time_rec_idx = (time_rec_idx + 1) % NUM_TIME_RECORDS

            # Write FPS to frame
            cv2.putText(frame, '%2.2f FPS' % (NUM_TIME_RECORDS / time_total), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))

            # Draw the original frame and our debugging frame in different windows
            cv2.imshow(VID_WIN_NAME, frame)
            cv2.imshow(OUT_WIN_NAME, mask)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        self.source.release()
