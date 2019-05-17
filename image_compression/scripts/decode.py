import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import fftpack

def idct2(img):
    return fftpack.idct(fftpack.idct(img, axis=0, norm='ortho'), axis=1, norm='ortho')

def decode(img, path_to_save):
	print('decodeeee')