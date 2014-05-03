import logging

import cv2
import numpy as np
import serial

from .interface import ObjectDetector

class PixyArduinoDetector(ObjectDetector):
    'Uses an Arduino connected to a Pixy reporting back over serial line'

    def __init__(self, device):
        # Reuse same frame array, just zero out when done
        self.frame_ = np.zeros((240, 320, 3), np.uint8)
        self.frame_[:] = 0

        # Time out after 20 micro sec as that is the fastest rate of the Pixy
        self.serial = serial.Serial(device, timeout=1/50.)

    def frame(self):
        return self.frame_

    def object_location(self):
        # Zere out frame for new object
        self.frame_[:] = 0

        ser_data = self.serial.readline()

        if len(ser_data) > 0:
            # Data will look like:
            # block index,signature,x,y,width,height
            parts = ser_data.strip().split(',')
            if len(parts) == 6:
                _,_, x, y, width, height = [ int(p) for p in parts ]
                radius = min(width, height)
                cv2.circle(self.frame_, (x,y), radius, (0,0,255), radius)
                return (x,y), radius
            else:
                return None
        else:
            return None
