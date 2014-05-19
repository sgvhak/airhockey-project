#!/usr/bin/env python

import freenect
import sys

ctx = freenect.init()
dev = freenect.open_device(ctx, freenect.num_devices(ctx) - 1)

freenect.set_tilt_degs(dev, int(sys.argv[1]))
