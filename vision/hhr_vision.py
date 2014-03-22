#!/usr/bin/python

import os
import sys
from ConfigParser import ConfigParser

import cv2
import numpy as np

# Which video device to use
VIDEO_SOURCE = 1

# Names for various named windows
VID_WIN_NAME = 'HHR - Video'
THRESH_WIN_NAME = 'HHR - Thresholds'
OUT_WIN_NAME = 'HHR - Output'

# Names to use for the HSV color channels in track bars
HSV_NAMES = ('H', 'S', 'V')
HSV_MAX_VALS = (180, 255, 255)

# Name of the min and max in the HSV trackbars
MIN_BAR_NAME = "min"
MAX_BAR_NAME = "max"

CONFIG_FILENAME = os.path.join(os.path.dirname(sys.argv[0]), "vision.cfg")
HSV_CONFIG_SECTION_PREFIX = "HSV"

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

def load_hsv_trackbars_values(window_name, config):
    for color_name in HSV_NAMES:
        for bar_name in (MIN_BAR_NAME, MAX_BAR_NAME):
            section_name = '%s %s' % (HSV_CONFIG_SECTION_PREFIX, bar_name)
            if config.has_option(section_name, color_name):
                bar_val = config.get(section_name, color_name)
                cv2.setTrackbarPos('%s %s' % (color_name, bar_name), window_name, int(bar_val))

def save_hsv_trackbars_values(window_name, config):
    for color_name in HSV_NAMES:
        for bar_name in (MIN_BAR_NAME, MAX_BAR_NAME):
            section_name = '%s %s' % (HSV_CONFIG_SECTION_PREFIX, bar_name)
            if not config.has_section(section_name):
                config.add_section(section_name) 
            bar_val = cv2.getTrackbarPos('%s %s' % (color_name, bar_name), window_name)
            config.set(section_name, color_name, str(bar_val))

def hsv_values(window_name, bar_type):
    hsv_vals = []
    for color_name in HSV_NAMES:
        hsv_vals.append( cv2.getTrackbarPos('%s %s' % (color_name, bar_type), window_name) )
    return np.array(hsv_vals)

def hsv_min_values():
    return hsv_values(THRESH_WIN_NAME, MIN_BAR_NAME)

def hsv_max_values():
    return hsv_values(THRESH_WIN_NAME, MAX_BAR_NAME)

def create_windows():
    cv2.namedWindow(VID_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(THRESH_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(OUT_WIN_NAME, cv2.WINDOW_AUTOSIZE)

    add_hsv_trackbars(THRESH_WIN_NAME)

## ALG Stuff ##

def capture_loop():
    cap = cv2.VideoCapture(1)

    while(True):
        # Capture frame-by-frame
        ret, oframe = cap.read()

        # Our operations on the frame come here
        tframe = oframe.copy()

        tframe = cv2.GaussianBlur(tframe, (5,5), 0)
        thsv = cv2.cvtColor(tframe, cv2.COLOR_BGR2HSV);

        hsv_min = hsv_min_values()
        hsv_max = hsv_max_values()

        mask = cv2.inRange(thsv, hsv_min, hsv_max)

        contours, hierarchy = cv2.findContours(mask.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        
        largest_cnt = None
        largest_area = -1 
        for cnt in contours:
            curr_area = cv2.contourArea(cnt)
            if curr_area > largest_area:
                largest_cnt = cnt

        shape_overlay = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        #cv2.drawContours(shape_img, [cnt], 0, (0,0,255), 3)
        (x,y), radius = cv2.minEnclosingCircle(largest_cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(shape_overlay, center,radius,(255,0,0),2)

        cv2.imshow(VID_WIN_NAME, oframe)
        cv2.imshow(OUT_WIN_NAME, shape_overlay)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()

def main():
    config = ConfigParser()
    config.read(CONFIG_FILENAME)

    create_windows()

    load_hsv_trackbars_values(THRESH_WIN_NAME, config)

    capture_loop()

    save_hsv_trackbars_values(THRESH_WIN_NAME, config)

    cv2.destroyAllWindows()

    config.write(open(CONFIG_FILENAME, "w"))

if __name__ == "__main__":
    main()
