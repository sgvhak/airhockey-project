#!/usr/bin/python

import cv2
import numpy as np

cap = cv2.VideoCapture(1)

VID_WIN_NAME = 'video'
THRESH_WIN_NAME = 'Thresholded'

cv2.namedWindow(VID_WIN_NAME)
cv2.namedWindow(THRESH_WIN_NAME)

# Empty call back for trackbars
def nothing(x):
    pass

# create trackbars for color range
cv2.createTrackbar('H min',THRESH_WIN_NAME, 0, 180,nothing)
cv2.createTrackbar('H max',THRESH_WIN_NAME, 0, 180,nothing)
cv2.setTrackbarPos('H max', THRESH_WIN_NAME, 180)

cv2.createTrackbar('S min',THRESH_WIN_NAME,0,255,nothing)
cv2.createTrackbar('S max',THRESH_WIN_NAME,0,255,nothing)
cv2.setTrackbarPos('S max', THRESH_WIN_NAME, 255)

cv2.createTrackbar('V min',THRESH_WIN_NAME,0,255,nothing)
cv2.createTrackbar('V max',THRESH_WIN_NAME,0,255,nothing)
cv2.setTrackbarPos('V max', THRESH_WIN_NAME, 255)

while(True):
    # Capture frame-by-frame
    ret, oframe = cap.read()

    # Our operations on the frame come here
#    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    tframe = oframe.copy()

    tframe = cv2.GaussianBlur(tframe, (5,5), 0)
    thsv = cv2.cvtColor(tframe, cv2.COLOR_BGR2HSV);

    hsv_min = np.array([ cv2.getTrackbarPos('H min',THRESH_WIN_NAME),
                         cv2.getTrackbarPos('S min',THRESH_WIN_NAME),
                         cv2.getTrackbarPos('V min',THRESH_WIN_NAME),])
    hsv_max = np.array([ cv2.getTrackbarPos('H max',THRESH_WIN_NAME),
                         cv2.getTrackbarPos('S max',THRESH_WIN_NAME),
                         cv2.getTrackbarPos('V max',THRESH_WIN_NAME),])

    mask = cv2.inRange(thsv, hsv_min, hsv_max)

    cv2.imshow(VID_WIN_NAME, oframe)
    cv2.imshow(THRESH_WIN_NAME, mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
