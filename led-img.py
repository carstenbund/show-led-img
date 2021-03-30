#
# Display image files on LED matrix 64x64
# get master image: wget https://www.larvalabs.com/public/images/cryptopunks/punks.png
# needs rgbmatrix : https://github.com/hzeller/rpi-rgb-led-matrix/tree/master/bindings/python
#

IMAGES = "adriana/*.png"

import sys
sys.path.insert(0, "/home/carsten/.local/lib/python3.7/site-packages")
#print(sys.path)

import os, time
from glob import glob
import cv2
import numpy as np
import random
from PIL import Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
options.gpio_slowdown = 4
options.panel_type = "FM6126A"

matrix = RGBMatrix(options = options)
matrix.brightness = 100


def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def load_image(img_name):
    img = cv2.imread(img_name)
    return img


def fit_to_width(img, x=64,y=64):
    print("w ", img.shape)
    res = ResizeWithAspectRatio(img,width=y)
    print('re ', res.shape)
    #return crop_img(res)
    return res

def crop_center(img,cropx,cropy):
    y,x,_ = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)
    ret = img[starty:starty+cropy,startx:startx+cropx]
    return ret

def crop_img(image,x=64,y=64):
    #cri = image[0:screen_width,0:screen_height]
    cri = crop_center(img,x,y)
    #cri = image[0:x,0:y]
    print("cropped : ",cri.shape)
    return cri


dir_path = os.path.dirname(os.path.realpath(__file__))
folder = dir_path + "/images/" +  IMAGES

img_arr = glob(folder)

n=1
while True:
    img_name = random.choice(img_arr)
    img = load_image(img_name)
    print(img_name)
    #img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = fit_to_width(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #imgwrite(img, )
    #img_32 = cv2.resize(img,(32,32), interpolation = cv2.INTER_NEAREST)
    img = Image.fromarray(img)
    matrix.SetImage(img)
    time.sleep(random.random()*9+1)
    #time.sleep(2)


