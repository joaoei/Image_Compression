import numpy as np
import cv2, math
from scripts import zigzag
from scipy import fftpack

def idct2(img):
    return fftpack.idct(fftpack.idct(img, axis=0, norm='ortho'), axis=1, norm='ortho')

def decode(img, path_to_save):
	name_file_full = img.split("/")[-1]
	name_file = name_file_full[0:-4]
	ext = name_file_full.split(".")[-1]

	if ext != "rle":
		raise Exception("File with extension other than .rle")

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

	file = open(img, "r")
	#file = open("image.rle","r")
	line = file.readline()
	data = line.split()
	file.close()

	image = np.zeros(int(data[0])*int(data[1])).astype(int)

	i = 2
	j = 0
	while i < len(data) and data[i] != ';':
		for k in range(int(data[i+1]) + 1):
			image[j] = int(data[i])
			j = j + 1

		i = i + 2

	image = np.reshape(image, (int(data[0]), int(data[1]) ))

	h = int(data[0])
	w = int(data[1])
	nbh = math.ceil(h/block_size)
	nbh = np.int32(nbh)
	nbw = math.ceil(w/block_size)
	nbw = np.int32(nbw)

	decode_img = np.zeros((h, w))
	decode_img[0:h, 0:w] = image[0:h, 0:w]

	for i in range(nbh):
		for j in range(nbw):
			# j-esimo block da imagem
			block = decode_img[i*block_size : (i*block_size) + block_size, j*block_size : (j*block_size) + block_size]
			
			# Transforma o bloco 8x8 em um array
			#block = block.flatten()
			
			# Aplicar o algoritmo de zigzag para reordenar os valores em um vetor
			#reordered = zigzag.inverse_zigzag(block, int(block_size), int(block_size))
			reordered = block

			# Dividir pela matriz de quantização
			quant = np.multiply(reordered, QUANTIZATION_MAT).astype(int)

			# Aplica dct no bloco
			idct = idct2(quant)

			# Salva os novos valores na imagem codificada
			decode_img[i*block_size : (i*block_size) + block_size, j*block_size : (j*block_size) + block_size] = idct

	decode_img[decode_img > 255] = 255
	decode_img[decode_img < 0] = 0

	cv2.imwrite(path_to_save+name_file, np.uint8(decode_img))

	cv2.imshow('decode image', np.uint8(decode_img))
	cv2.waitKey(0)
	cv2.destroyAllWindows()