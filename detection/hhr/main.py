import logging
import cv2

from .calc import MovingAverage
from .gui import VID_WIN_NAME
  
# How many time values to save for averaging for calculating FPS
NUM_TIME_RECORDS = 5

def main_loop(detector, predictor, controller):
    time_avg = MovingAverage(NUM_TIME_RECORDS)
    while(True):
        time_tick_beg = cv2.getTickCount()

        # Get frame which can be drawn on
        frame = detector.frame()

        # Check if there is a detected object
        detect_res = detector.object_location()

        # Predict movement and inform controller where to intercept
        if detect_res:
            coords, radius = detect_res 
            predictor.add_puck_event(cv2.getTickCount() / cv2.getTickFrequency(), coords, radius)
            i_point = predictor.intercept_point()

            if controller:
                controller.move_to(i_point)

        # Draw predictor information
        predictor.draw(frame)

        elapsed_time = (cv2.getTickCount() - time_tick_beg) / cv2.getTickFrequency()
        time_avg.add_value(elapsed_time)

        # Write FPS to frame
        cv2.putText(frame, '%2.2f FPS' % (1/time_avg.average), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255))

        # Draw frame with possibly video and other information drawn on top
        cv2.imshow(VID_WIN_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
