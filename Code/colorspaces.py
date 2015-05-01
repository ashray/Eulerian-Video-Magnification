from __future__ import division, print_function
import numpy as np
import cv2
from common import nothing, getsize

def rgb2ntsc(R,G,B):
    Y = 0.299*R + 0.587*G + 0.114*B
    I = 0.596*R - 0.274*G - 0.322*B
    Q = 0.211*R - 0.523*G + 0.312*B
    return Y,I,Q

def ntsc2rgb(Y,I,Q):
    R = 1.000*Y + 0.956*I + 0.621*Q
    G = 1.000*Y + -0.272*I + -0.647*Q
    B = 1.000*Y + -1.106*I + 1.703*Q
    return R,G,B

def extract_tuples(frame):
    T1 = frame[:,:,0]
    T2 = frame[:,:,1]
    T3 = frame[:,:,2]
    return T1,T2,T3

def convert_rgb_frame_to_ntsc(frame):
    dtype = frame.dtype
    result = np.ndarray(shape=frame.shape, dtype=dtype)
    np.copyto(result, frame)
    R,G,B = extract_tuples(frame)
    Y,I,Q = rgb2ntsc(R,G,B)
    result[:,:,0] = Y
    result[:,:,1] = I
    result[:,:,2] = Q
    return result

def convert_ntsc_frame_to_rgb(frame):
    dtype = frame.dtype
    result = np.ndarray(shape=frame.shape, dtype=dtype)
    np.copyto(result, frame)
    Y,I,Q = extract_tuples(frame)
    R,G,B = ntsc2rgb(Y,I,Q)
    result[:,:,0] = R
    result[:,:,1] = G
    result[:,:,2] = B
    return result

def test_conversions(frame):
    frame_ntsc = convert_rgb_frame_to_ntsc(frame)
    frame_recons = convert_ntsc_frame_to_rgb(frame_ntsc)
    # there is a small loss of accuracy in the conversion process
    assert(np.all(frame - frame_recons < 1e-2))

def grab_frame(capture):
    _, frame = capture.read()
    return None if frame is None else frame / frame.max()

def show_image(image, window_name='test'):
    while True:
        cv2.imshow(window_name, image)
        if (cv2.waitKey(1) & 0xFF) == 27:
            exit(0)

def build_lappyr(img, leveln=6, dtype=np.int16):
    levels = []
    for i in xrange(leveln-1):
        next_img = cv2.pyrDown(img)
        img1 = cv2.pyrUp(next_img, dstsize=getsize(img))
        levels.append(img-img1)
        img = next_img
    levels.append(img)
    return np.array(levels)

def merge_lappyr(levels):
    img = levels[-1]
    for lev_img in levels[-2::-1]:
        img = cv2.pyrUp(img, dstsize=getsize(lev_img))
        img += lev_img
    return img

def make_grayscale_pixel(r,g,b):
    return (r+g+b)/3

def make_grayscale(frame):
    w, h = len(frame[0]), len(frame)
    result = np.zeros([h, w])
    for x in xrange(w):
        for y in xrange(h):
            rgb = frame[y][x]
            result[y][x] = make_grayscale_pixel(*rgb)
    return result