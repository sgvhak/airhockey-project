#include <iomanip>

#include "opencv2/opencv.hpp"

#define DFLT_VIDEO_SOURCE 0
#define NUM_TIME_RECORDS 5
#define VID_WIN_NAME "Video"

using namespace cv;

int main(int argc, char* argv[]) {
    int vid_source = DFLT_VIDEO_SOURCE;
    if (argc > 1)
        vid_source = atoi(argv[1]);
    VideoCapture cap(vid_source);
    if(!cap.isOpened())  // check if we succeeded
        exit(1);

    double time_records[NUM_TIME_RECORDS] = {0};
    int time_rec_idx = 0;
    double time_total = 0;
    while (true) {
        double time_beg = getTickCount();

        // Capture frame-by-frame
        Mat frame;
        cap >> frame;

        double time_end = (getTickCount() - time_beg) / getTickFrequency();

        // Record time value in a rolling sum where the oldest falls off
        // This way we can smooth out the FPS value
        double oldest_val = time_records[time_rec_idx];
        if (oldest_val > 0)
            time_total -= oldest_val;
        time_total += time_end;
        time_records[time_rec_idx] = time_end;
        time_rec_idx = (time_rec_idx + 1) % NUM_TIME_RECORDS;

        // Write FPS to frame
        std::stringstream fps_str;
        fps_str << std::setprecision(4) << (NUM_TIME_RECORDS / time_total) << " FPS";
        putText(frame, fps_str.str(), Point(10, 30), FONT_HERSHEY_SIMPLEX, 1, Scalar::all(255));

        imshow(VID_WIN_NAME, frame);

        if (waitKey(1) == ('q'))
            break;
    }

    // When everything done, release the capture
    cap.release();
}
