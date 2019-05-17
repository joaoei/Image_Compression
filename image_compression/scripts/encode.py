import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
from scipy import fftpack

def dct2(img):
    return fftpack.dct(fftpack.dct(img, axis=0, norm='ortho'), axis=1, norm='ortho')

def encode(img_path, path_to_save):
	img = cv2.imread(img_path, 0).astype(int)
	
	print('encodeeee')