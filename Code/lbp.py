# compute local binary patterns for an image
# useful reference: http://www.bytefish.de/blog/local_binary_patterns/

from __future__ import division, print_function
from colorspaces import *
import pdb
import numpy as np
import cv2
import video
import sys

# im = image
# p = number of sampling points
# r = radius of sampling circle
def lbp(im, p, r):
    '''Compute LBP for an image'''
    w, h = len(im[0]), len(im)
    hist = [0] * (1 << p)
    for y in xrange(r, h-r):
        for x in xrange(r, w-r):
            val = lbp_pixel(im, p, r, x, y)
            hist[val] += 1
    return squash_histogram(hist)

def squash_histogram(hist):
    '''Remove all entries of the histogram consisting
    of non-zero entries'''
    # for idx, freq in enumerate(hist):
    #     if freq != 0:
    #         print(bin(idx)[2:].rjust(8,'0'))
    result = []
    for (idx, entry) in enumerate(hist):
        binstring = bin(idx)[2:].rjust(8,'0')
        pattern = map(int, list(binstring))
        if num_transitions(pattern) <= 2:
            print(binstring)
            result.append(entry)
    print(len(result))
    return result

def joint_lbp_histogram(im):
    '''Create the joint LBP histogram for a frame
    as described in the paper'''
    return lbp(im, 8, 1)
    # return lbp(im, 8, 1) + lbp(im, 8, 2) + lbp(im, 16, 1)

def num_transitions(pattern):
    '''Find the number of transitions from 0 to 1 or vice-versa
    in a circular bit pattern given as a list'''
    rotated = pattern[1:] + [pattern[0]]
    result = sum(x != y for x,y in zip(pattern, rotated))
    return result

def lbp_pixel(im, p, r, x, y):
    '''Compute LBP for a pixel of an image'''
    c = (x+0.5, y+0.5) # center of the circle
    intens_cent = intensity_at(im, c[0], c[1])
    angles = np.linspace(0, 2*np.pi, p)
    samples = [intensity_at(im, c[0] + np.sin(th), c[1] - np.cos(th)) for th in angles]
    pattern = [int(sample >= intens_cent) for sample in samples]
    return 255 if num_transitions(pattern) > 2 else int(''.join(map(str, reversed(pattern))), 2)
    # return (p*(p-1))+3 if num_transitions(pattern) > 2 else int(''.join(map(str, reversed(pattern))), 2)

def intensity_at(im, x, y):
    '''Compute intensity at a point inside an image using bilinear interpolation
    Convention: intensity_at(1.5,6.5) == pixel value of pixel (1,6)'''
    x_l = np.floor(x) + .5 # left x
    x_r = x_l + 1 # right x
    y_t = np.floor(y) + .5 # top y
    y_b = y_t + 1 # bottom y
    s = x - x_l
    t = y - y_t
    term1 = 0 if s == 0 or t == 0 else intens_helper(im,y_b-.5,x_r-.5)
    term2 = 0 if s == 0 or t == 1 else intens_helper(im,y_t-.5,x_r-.5)
    term3 = 0 if s == 1 or t == 0 else intens_helper(im,y_b-.5,x_l-.5)
    term4 = 0 if s == 1 or t == 1 else intens_helper(im,y_t-.5,x_l-.5)
    return s*(t*term1 + (1-t)*term2) + (1-s)*(t*term3 + (1-t)*term4)

def intens_helper(im, x, y):
    w, h = len(im[0]), len(im)
    if x >= w or y >= h or x < 0 or y < 0:
        return 0
    return im[y][x]
    
if __name__ == '__main__':
    # print(num_transitions([1,0,0,0]))
    filename = sys.argv[1]
    cap = video.create_capture(filename)
    frame = grab_frame(cap)
    frame = make_grayscale(frame)
    print(joint_lbp_histogram(frame))