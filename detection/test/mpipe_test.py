#!/usr/bin/env python

import mpipe
import cv2
import sys
import numpy as np

VIDEO_SOURCE = int(sys.argv[1]) 
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
NUM_TIME_RECORDS = 5

class DisplayWorker(mpipe.OrderedWorker):
    def __init__(self):
        mpipe.OrderedWorker.__init__(self)
        self.time_records = np.zeros(NUM_TIME_RECORDS, float)
        self.time_rec_idx = 0
        self.time_total = 0
        self.last_time = cv2.getTickCount()
    
    def doTask(self, frame):
        time_now = cv2.getTickCount()
        time_end = (time_now - self.last_time) / cv2.getTickFrequency()

        # Record time value in a rolling sum where the oldest falls off
        # This way we can smooth out the FPS value
        oldest_val = self.time_records[self.time_rec_idx]
        if oldest_val > 0:
            self.time_total -= oldest_val 
        self.time_total += time_end 
        self.time_records[self.time_rec_idx] = time_end
        self.time_rec_idx = (self.time_rec_idx + 1) % NUM_TIME_RECORDS
    
        # Write FPS to frame
        #cv2.putText(frame, '%2.2f FPS' % (1 / time_end), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        cv2.putText(frame, '%2.2f FPS' % (NUM_TIME_RECORDS / self.time_total), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))

        cv2.imshow("Video", frame)

        self.last_time = cv2.getTickCount()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        else:
            return True

stage = mpipe.Stage(DisplayWorker)
#stage = mpipe.FilterStage((mpipe.Stage(DisplayWorker),), max_tasks=1000, drop_results=True)

pipe = mpipe.Pipeline(stage)

cap = cv2.VideoCapture(VIDEO_SOURCE)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
while True:
    ret, frame = cap.read()
    pipe.put(frame)
