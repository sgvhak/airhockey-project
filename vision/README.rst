SGVHAK Air Hockey Robot Player
==============================

Installation
------------

The first dependency to worry about it OpenCV. It must be installed from a distribution package or from source. The Python bindings are not in PyPi and do not use the standard setuputils code to compile. Therefore if using Ubuntu, install this package, or find the equivalent for your distro::

    sudo apt-get install python-opencv

For some of the other requirements you may choose to use the version from your distributions repos::
    
    sudo apt-get install python-pygame python-numpy

We also need pymunk, but there is no package in Ubuntu for it. You can install it using pip::

    sudo pip install pymunk

If you'd rather just use a virtualenv, then build one that uses the distribution's version of opencv's bindings. Then use pip to install the requirements::

    pip install -r requirements.txt

Or install this Python module and let setup utils do the work of resolving dependencies::

    python setup.py install

Usage
-----

The robot player is launched using the hhr.py script. It has a help message -h that explains most options. To get started run it specifying the video devices to use. Use an integer for v4l devices::

    hhr.py -s 0

If you do not have a camera, be sure to indicate that cv2 should use a simulated camera::

    hhr.py -s sim
