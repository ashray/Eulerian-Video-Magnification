About
-----

OpenCV implementation of http://people.csail.mit.edu/mrub/papers/vidmag.pdf

Dependencies
------------

numpy, opencv, avconv

Running the code
----------------

    ./magnify-video.sh <filter_type> <video_name> <magnification_factor>

1. The last parameter is optional, and defaults to 2.
2. `filter_type` is either `iir` or `butter`.
3. `video_name` makes the script search for a video named `./input/<video_name>`.
4. The output will be produced in the folder `./output/<filter_type>/<video_name>-<magnification_factor>.mp4`.

Example
----------------

If you want to magnify a baby.mp4 video, then make a folder named "input" inside the code folder and copy the input video, in this case baby.mp4 inside the input folder.
Then run 

    ./magnify-video.sh iir baby.mp4 20

The output video, in this case will be generated in `./output/iir/baby-20.mp4`
