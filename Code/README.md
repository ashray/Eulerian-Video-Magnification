About
-----

OpenCV implementation of http://people.csail.mit.edu/mrub/papers/vidmag.pdf

Dependencies
------------

numpy, opencv

Running the code
----------------

    ./magnify-video.sh <filter_type> <video_name> <magnification_factor>

1. The last parameter is optional, and defaults to 2.
2. `filter_type` is either `iir` or `butter`.
3. `video_name` makes the script search for a video named `./input/<video_name>.mp4`.
4. The output will be produced in the folder `./output/<filter_type>/<video_name>-<magnification_factor>.mp4`.
