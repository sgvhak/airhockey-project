import logging
from abc import abstractmethod

import cv2
import numpy as np

from .interface import ObjectDetector

class PixyDetector(ObjectDetector):

    def __init__(self, signature=1):
        # Signature of the object to use
        self.signature = signature

        # Reuse same frame array, just zero out when done
        self.frame_ = np.zeros((240, 320, 3), np.uint8)
        self.frame_[:] = 0


    def frame(self):
        return self.frame_

    @abstractmethod
    def objects(self):
        'Returns tuple of detection data: signature, x, y, width, height'
        pass

    def object_location(self):
        # Zero out frame for new object since we draw the detected circle
        self.frame_[:] = 0

        for p_obj in self.objects():
            sig, x, y, width, height = p_obj
            if sig == self.signature:
                radius = min(width, height)
                cv2.circle(self.frame_, (x,y), radius, (0,0,255), -1)
                return (x,y), radius
        return None

class PixyArduinoDetector(PixyDetector):
    'Uses an Arduino connected to a Pixy reporting back over serial line'

    def __init__(self, device, **kwargs):
        import serial

        super(PixyArduinoDetector, self).__init__(**kwargs)

        # Time out after 20 micro sec as that is the fastest rate of the Pixy
        self.serial = serial.Serial(device, timeout=1/50.)

    def objects(self):
        ser_data = self.serial.readline()
        if len(ser_data) > 0:
            # Data will look like:
            # block index,signature,x,y,width,height
            parts = ser_data.strip().split(',')
            if len(parts) == 6:
                try:
                    _,_, x, y, width, height = [ int(p) for p in parts ]

                    # Flush serial input otherwise it gets backlogged and coords lag
                    self.serial.flushInput()
                except ValueError:
                    # Error parsing parts and turning them into integers
                    return ()

        return ()

class PixyRPiDetector(PixyDetector):
    'Uses the Raspberry Pi SPI to talk to a Pixy'

    def __init__(self, max_attempts=4, **kwargs):
        from rpi.pixy import Pixy
        from rpi.pixy_spi import LinkSPI

        super(PixyRPiDetector, self).__init__(**kwargs)

        # Maximum number of empty blocks before giving up trying to
        # get objects
        self.max_attempts = max_attempts

        self.pixy_spi = Pixy(LinkSPI())

    def objects(self):
        attempts = 0
        while self.pixy_spi.getBlocks() == 0 and attempts < self.max_attempts:
            attempts += 1
        return self.pixy_spi.blocks
