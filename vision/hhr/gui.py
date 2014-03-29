import numpy as np
import cv2

from .interface import HSVThreshold

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

class HSVTrackBars(HSVThreshold):

    def __init__(self, window_name, config=None):
        self.window_name = window_name
        
        self._add_to_window()

        if config:
            self.load_config(config)

    def _add_to_window(self):
        # Empty call back for trackbars
        def nothing(x):
            pass

        # create trackbars for color range
        for color_name, max_value in zip(HSV_NAMES, HSV_MAX_VALS):
            cv2.createTrackbar('%s %s' % (color_name, MIN_BAR_NAME), self.window_name, 0, max_value, nothing)
            cv2.createTrackbar('%s %s' % (color_name, MAX_BAR_NAME), self.window_name, 0, max_value, nothing)
            cv2.setTrackbarPos('%s %s' % (color_name, MAX_BAR_NAME), self.window_name, max_value)

        cv2.createTrackbar('Enabled', self.window_name, 0, 1, nothing)

    def load_config(self, config):
        for color_name in HSV_NAMES:
            for bar_name in (MIN_BAR_NAME, MAX_BAR_NAME):
                section_name = '%s %s' % (self.window_name, bar_name)
                if config.has_option(section_name, color_name):
                    bar_val = config.get(section_name, color_name)
                    cv2.setTrackbarPos('%s %s' % (color_name, bar_name), self.window_name, int(bar_val))

    def save_config(self, config):
        for color_name in HSV_NAMES:
            for bar_name in (MIN_BAR_NAME, MAX_BAR_NAME):
                section_name = '%s %s' % (self.window_name, bar_name)
                if not config.has_section(section_name):
                    config.add_section(section_name) 
                bar_val = cv2.getTrackbarPos('%s %s' % (color_name, bar_name), self.window_name)
                config.set(section_name, color_name, str(bar_val))

    def enabled(self):
        enab_val = cv2.getTrackbarPos('Enabled', self.window_name)

        if enab_val:
            return True
        else:
            return False

    def values(self, bar_type):
        hsv_vals = []
        for color_name in HSV_NAMES:
            hsv_vals.append( cv2.getTrackbarPos('%s %s' % (color_name, bar_type), self.window_name) )
        return np.array(hsv_vals)

    def min_values(self):
        return self.values(MIN_BAR_NAME)

    def max_values(self):
        return self.values(MAX_BAR_NAME)

def create_windows():
    cv2.namedWindow(THRESH1_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(THRESH2_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(OUT_WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(VID_WIN_NAME, cv2.WINDOW_AUTOSIZE)

def create_trackbars(config):
    thresholds = []
    for tname in [THRESH1_WIN_NAME, THRESH2_WIN_NAME]:
        thresholds.append( HSVTrackBars(tname, config) )
    return thresholds

def destroy_windows():
    cv2.destroyAllWindows()
