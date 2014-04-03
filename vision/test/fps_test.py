#!/usr/bin/env python

import sys

import cv2
import numpy as np

VIDEO_SOURCE = len(sys.argv) > 1 and int(sys.argv[1]) or 0
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
NUM_TIME_RECORDS = 5
VID_WIN_NAME = 'Video'

cap = cv2.VideoCapture(VIDEO_SOURCE)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

time_records = np.zeros(NUM_TIME_RECORDS, float)
time_rec_idx = 0
time_total = 0
while(True):
    time_beg = cv2.getTickCount()

    # Capture frame-by-frame
    ret, frame = cap.read()

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

    cv2.imshow(VID_WIN_NAME, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
