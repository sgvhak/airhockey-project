SGVHAK Air Hockey Robot Player
==============================

Installation
------------

If using Ubuntu, install these packages, find the equivalent for your distro::

    apt-get install python-numpy python-opencv python-pygame

We also need pymunk, but there is no Ubuntu package for that. Install it using pip in a virtual env if you desire::

    pip install pymunk

If you do not have a camera, be sure to indicate that cv2 should use a simulated camera::

    ./hhr.py -s sim
