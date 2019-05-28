import numpy as np
import cv2, math
from scripts import zigzag
from scipy import fftpack

def RLE(image):
    skip = 0
    image = image.astype(int)
    string = ""
    prev = image[0]
    for i in range(1, image.shape[0]):
    	if image[i] != prev:
    		string = string + str(prev) + " " + str(skip) + " "
    		prev = image[i]
    		skip = 0
    	else:
    		skip = skip + 1

    string = string + str(prev) + " " + str(skip) + " "

    return string

def dct2(img):
    return fftpack.dct(fftpack.dct(img, axis=0, norm='ortho'), axis=1, norm='ortho')

def encode(img_path, path_to_save):
	img = cv2.imread(img_path, 0).astype(int)

	block_size = 8

	QUANTIZATION_MAT = np.array([
		[16,11,10,16,24,40,51,61],
		[12,12,14,19,26,58,60,55],
		[14,13,16,24,40,57,69,56],
		[14,17,22,29,51,87,80,62],
		[18,22,37,56,68,109,103,77],
		[24,35,55,64,81,104,113,92],
		[49,64,78,87,103,121,120,101],
		[72,92,95,98,112,100,103,99]
	])
	
	''' Image test

	img = np.array([
		[255, 255, 227, 204, 204, 203, 192, 217],
		[215, 189, 167, 166, 160, 135, 167, 244],
		[169, 115, 99,  99,  99,  82,  127, 220],
		[146, 90,  86,  88,  84,  63,  195, 189],
		[255, 255, 231, 239, 240, 182, 251, 232],
		[255, 255, 21,  245, 226, 169, 229, 247],
		[255, 255, 222, 251, 174, 209, 174, 163],
		[255, 255, 221, 184, 205, 248, 249, 220]])
	'''

	[h , w] = img.shape

	nbh = math.ceil(h/block_size)
	nbh = np.int32(nbh)
	nbw = math.ceil(w/block_size)
	nbw = np.int32(nbw)

	encoded_img = np.zeros((h, w))
	encoded_img[0:h, 0:w] = img[0:h, 0:w]

	# Get the name of file
	name_file = img_path.split("/")[-1]

	cv2.imwrite(name_file[0:-4]+".bmp", np.uint8(encoded_img))

	for i in range(nbh):
		for j in range(nbw):
			# j-esimo block da imagem
			block = encoded_img[i*block_size : (i*block_size) + block_size, j*block_size : (j*block_size) + block_size]

			# Calcular o dct no bloco
			dct = dct2(block)

			# Dividir pela matriz de quantização para quantizar os coeficientes e até eliminar alguns
			quant = np.divide(dct, QUANTIZATION_MAT).astype(int)
			
			# Aplicar o algoritmo de zigzag para reordenar os valores em um vetor
			#reordered = zigzag.zigzag(quant)

			#reshaped = np.reshape(reordered, (block_size, block_size)) 

			# Transforma para um bloco 8x8
			#new_block = reshaped
			
			new_block = quant
			# Salva os novos valores na imagem codificada
			encoded_img[i*block_size : (i*block_size) + block_size, j*block_size : (j*block_size) + block_size] = new_block

	arranged = encoded_img.flatten()

	string = RLE(arranged)
	string = str(encoded_img.shape[0]) + " " + str(encoded_img.shape[1]) + " " + string + ";"

	file = open(path_to_save+name_file+".rle", "w")
	file.write(string)
	file.close()