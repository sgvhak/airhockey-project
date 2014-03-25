#!/usr/bin/env python

import os
import sys
import logging
from ConfigParser import ConfigParser

import cv2
import numpy as np

# Which video device to use
VIDEO_SOURCE = len(sys.argv) > 1 and int(sys.argv[1]) or 0
CAPTURE_WIDTH = 320
CAPTURE_HEIGHT = 240

# Names for various named windows
VID_WIN_NAME = 'HHR - Video'
THRESH1_WIN_NAME = 'HHR - Thresholds 1'
THRESH2_WIN_NAME = 'HHR - Thresholds 2'
OUT_WIN_NAME = 'HHR - Output'

# Names to use for the HSV color channels in track bars
HSV_NAMES = ('H', 'S', 'V')
HSV_MAX_VALS = (180, 255, 255)

# Name of the min and max in the HSV trackbars
MIN_BAR_NAME = "Min"
MAX_BAR_NAME = "Max"

CONFIG_FILENAME = os.path.join(os.path.dirname(sys.argv[0]), "vision.cfg")

# How many time values to save for averaging for calculating FPS
NUM_TIME_RECORDS = 5

## GUI Stuff ##

def add_hsv_trackbars(window_name):
    # Empty call back for trackbars
    def nothing(x):
        pass

    # create trackbars for color range
    for color_name, max_value in zip(HSV_NAMES, HSV_MAX_VALS):
        cv2.createTrackbar('%s %s' % (color_name, MIN_BAR_NAME), window_name, 0, max_value, nothing)
        cv2.createTrackbar('%s %s' % (color_name, MAX_BAR_NAME), window_name, 0, max_value, nothing)
        cv2.setTrackbarPos('%s %s' % (color_name, MAX_BAR_NAME), window_name, max_value)

    cv2.createTrackbar('Enabled', window_name, 0, 1, nothing)

def load_hsv_trackbars_values(window_name, config):
    for color_name in HSV_NAMES:
        for bar_name in (MIN_BAR_NAME, MAX_BAR_NAME):
            section_name = '%s %s' % (window_name, bar_name)
            if config.has_option(section_name, color_name):
                bar_val = config.get(section_name, color_name)
                cv2.setTrackbarPos('%s %s' % (color_name, bar_name), window_name, int(bar_val))

def save_hsv_trackbars_values(window_name, config):
    for color_name in HSV_NAMES:
        for bar_name in (MIN_BAR_NAME, MAX_BAR_NAME):
            section_name = '%s %s' % (window_name, bar_name)
            if not config.has_section(section_name):
                config.add_section(section_name) 
            bar_val = cv2.getTrackbarPos('%s %s' % (color_name, bar_name), window_name)
            config.set(section_name, color_name, str(bar_val))

def hsv_trackbars_enabled(window_name):
    enab_val = cv2.getTrackbarPos('Enabled', window_name)

    if enab_val:
        return True
    else:
        return False

def hsv_values(window_name, bar_type):
    hsv_vals = []
    for color_name in HSV_NAMES:
        hsv_vals.append( cv2.getTrackbarPos('%s %s' % (color_name, bar_type), window_name) )
    return np.array(hsv_vals)

def create_windows():
    cv2.namedWindow(THRESH1_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(THRESH2_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(OUT_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(VID_WIN_NAME, cv2.WINDOW_AUTOSIZE)

## ALG Stuff ##

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
        x, y = -1, -1
        try:
            if largest_cnt != None:
                (x, y), radius = cv2.minEnclosingCircle(largest_cnt)
                center = (int(x), int(y))
                radius = int(radius)

                cv2.circle(mask, center,radius, circle_color, 2)
        except cv2.error as exc:
            # Errors will also be displayed by the C++ part
            logging.error("Failure to find enclosing circle")

        return (x,y), mask

def capture_loop():
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

    time_records = np.zeros(NUM_TIME_RECORDS, float)
    time_rec_idx = 0
    time_total = 0
    while(True):
        time_beg = cv2.getTickCount()

        # Capture frame-by-frame
        ret, frame = cap.read()

        if hsv_trackbars_enabled(THRESH1_WIN_NAME):
            hsv1_min = hsv_values(THRESH1_WIN_NAME, MIN_BAR_NAME)
            hsv1_max = hsv_values(THRESH1_WIN_NAME, MAX_BAR_NAME)

            coords1, mask1 = detect_circular_object(frame, hsv1_min, hsv1_max, (255,0,0))
        else:
            mask1 = np.zeros(frame.shape, np.uint8)

        if hsv_trackbars_enabled(THRESH2_WIN_NAME):
            hsv2_min = hsv_values(THRESH2_WIN_NAME, MIN_BAR_NAME)
            hsv2_max = hsv_values(THRESH2_WIN_NAME, MAX_BAR_NAME)

            coords2, mask2 = detect_circular_object(frame, hsv2_min, hsv2_max, (0,255,0))
        else:
            mask2 = np.zeros(frame.shape, np.uint8)

        mask_combined = cv2.add(mask1, mask2)

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
        cv2.putText(frame, '%2.2f FPS' % (NUM_TIME_RECORDS / time_total), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

        # Draw the original frame and our debugging frame in different windows
        cv2.imshow(VID_WIN_NAME, frame)
        cv2.imshow(OUT_WIN_NAME, mask_combined)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

def main():
    config = ConfigParser()
    config.read(CONFIG_FILENAME)

    create_windows()
    add_hsv_trackbars(THRESH1_WIN_NAME)
    add_hsv_trackbars(THRESH2_WIN_NAME)

    load_hsv_trackbars_values(THRESH1_WIN_NAME, config)
    load_hsv_trackbars_values(THRESH2_WIN_NAME, config)

    capture_loop()

    save_hsv_trackbars_values(THRESH1_WIN_NAME, config)
    save_hsv_trackbars_values(THRESH2_WIN_NAME, config)

    cv2.destroyAllWindows()

    config.write(open(CONFIG_FILENAME, "w"))

if __name__ == "__main__":
    main()
