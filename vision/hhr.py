#!/usr/bin/env python

import os
import sys
from ConfigParser import ConfigParser
import argparse

from hhr import gui, vision

# Default values for command line arguments
DFLT_CAPTURE_SOURCE = 0
DFLT_CAPTURE_WIDTH = 320
DFLT_CAPTURE_HEIGHT = 240
DFLT_CONFIG_FILENAME = os.path.join(os.path.dirname(sys.argv[0]), "vision.cfg")

def main():
    parser = argparse.ArgumentParser(description='SGVHAK Hockey Robot Player')

    parser.add_argument('-c', '--config', dest='config_filename',
                        metavar='FILENAME', default=DFLT_CONFIG_FILENAME,
                        help='Configuration file to use, default: %s' % DFLT_CONFIG_FILENAME)
    parser.add_argument('--width', dest='capture_width',
                        metavar='INT', type=int, default=DFLT_CAPTURE_WIDTH,
                        help='Width of the frame to capture from the image source')
    parser.add_argument('--height', dest='capture_height',
                        metavar='INT', type=int, default=DFLT_CAPTURE_HEIGHT,
                        help='Height of the frame to capture from the image source')
    parser.add_argument('-s', '--source', dest='capture_source',
                        default=DFLT_CAPTURE_SOURCE,
                        help='Source to capture frames from. Either an integer for a video source or "sim" for the simulator')

    args = parser.parse_args()

    config = ConfigParser()
    config.read(args.config_filename)

    gui.create_windows()

    thresholds = gui.create_trackbars(config)

    source = None
    if type(args.capture_source) is int or args.capture_source.isdigit():
        source = vision.CV2CaptureSource(int(args.capture_source), args.capture_width, args.capture_height)
    elif args.capture_source.lower() == "sim":
        source = vision.SimulatedCaptureSource(args.capture_width, args.capture_height)
    else:
        parser.error("Unknown capture source: %s" % args.capture_source)

    vis = vision.Vision(source, thresholds)
    vis.capture_loop()

    for thresh in thresholds:
        thresh.save_config(config)

    gui.destroy_windows()

    config.write(open(args.config_filename, "w"))

if __name__ == "__main__":
    main()
