#!/usr/bin/env python

from __future__ import print_function, division
import pdb
import numpy as np
import scipy
from scipy.signal import butter
import cv2
import video
import sys
from common import nothing, getsize
from colorspaces import *
import os

alpha = 20
lambda_c = 80
delta = lambda_c/8/(1+alpha)
exaggeration_factor = int(sys.argv[2])
fl = 0.5
fh = 10
samplingRate = 30
r1 = 0.4
r2 = 0.05
chromAttenuation = 0

try:
    fn = sys.argv[1]
except:
    fn = 0

low_a, low_b = scipy.signal.butter(1, fl/samplingRate, 'low');
high_a, high_b = scipy.signal.butter(1, fh/samplingRate, 'low');

print('Exaggeration factor:', exaggeration_factor)

cap = video.create_capture(fn)
leveln = 6
# cv2.namedWindow('level control')
# for i in xrange(leveln):
#     cv2.createTrackbar('%d'%i, 'level control', 5, 50, nothing)

frame = grab_frame(cap)
frame_ntsc = convert_rgb_frame_to_ntsc(frame)

test_conversions(frame)

pyr = build_lappyr(frame_ntsc, leveln)

lowpass1 = pyr
lowpass2 = pyr
pyr_prev = pyr

output_frames = []

iter = 0
while True:
    iter += 1
    print(iter, end=' ')
    frame = grab_frame(cap)
    if frame is None:
        break
    frame_ntsc = convert_rgb_frame_to_ntsc(frame)
    pyr = build_lappyr(frame_ntsc, leveln)

    lowpass1 = (-high_b[1]*lowpass1 + high_a[0]*pyr + high_a[1]*pyr_prev)/high_b[0]
    lowpass2 = (-low_b[1]*lowpass2 + low_a[0]*pyr + low_a[1]*pyr_prev)/low_b[0]
    filtered = lowpass1 - lowpass2

    pyr_prev = pyr

    # print(filtered)

    h, w, _ = frame.shape
    lambda_vid = ((h**2 + w**2)**0.5)/3 # 3 is experimental constant

    # ignore the highest and lowest frequencies
    for i in [leveln-1, 0]:
        filtered[i] = np.zeros(filtered[i].shape)

    for i in xrange(leveln-2,0,-1):
        currAlpha = lambda_vid/delta/8 - 1
        currAlpha = currAlpha * exaggeration_factor
        filtered[i] = (alpha if currAlpha > alpha else currAlpha) * filtered[i]
        lambda_vid /= 2

    output_frame = merge_lappyr(filtered)
    output_frame[:,:,1] = output_frame[:,:,1] * chromAttenuation
    output_frame[:,:,2] = output_frame[:,:,2] * chromAttenuation

    # print(output_frame)

    output_frame = output_frame + frame_ntsc
    output_frame = convert_ntsc_frame_to_rgb(output_frame)

    output_frames.append(output_frame)

cap.release()

for idx, frame in enumerate(output_frames):
    cv2.imwrite('frames/output_' + str(idx) + '.png', frame * 255)

# os.system("avconv -i frames/output_%d.png -r 30 -b 65536k magnified.mp4")
