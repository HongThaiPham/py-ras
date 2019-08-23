import cv2
from primesense import openni2
from primesense import _openni2 as c_api
import os
import numpy as np
import time

dist = os.path.join("C:\OpenNI\Windows", "Redist")
openni2.initialize(dist)
dev = openni2.Device.open_any()
rgb_stream = dev.create_color_stream()
rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=60))
rgb_stream.start()

depth_stream = dev.create_depth_stream()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX=320, resolutionY=240, fps=30))
depth_stream.start()

def get_rgb():
    """
    Returns numpy 3L ndarray to represent the rgb image.
    """
    bgr = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(240, 320, 3)
    rgb = cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB)
    return rgb    

def get_depth():
    dXa = 1000.0
    dGan = 100.0
    dmap = np.fromstring(depth_stream.read_frame().get_buffer_as_uint16(),dtype=np.uint16).reshape(240, 320)
    dmap[(dmap > dXa) | (dmap < dGan)] = 0.0
    dmap[(dmap < dXa) & (dmap > dGan)] = 255.0
    img = dmap.astype(np.uint8)
    return img

while 1:
    rgb = get_rgb()
    depth = get_depth()
    
    cv2.imshow("rgb", rgb)
    cv2.imshow("depth", depth)
    cv2.waitKey(1)