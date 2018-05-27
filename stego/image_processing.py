from PIL import Image, ImageDraw
import random
import itertools
from stego.container import Container

def flip(i, j):
	#реализует lsb matching
	if j == 1:
		if i == 0:
			return 1
		elif i == 255:
			return -1
		else: 
			return (1-2*(random.getrandbits(1)))
	else: 
		return 0

def get_lsb(pix):
	#возвращзает младшие биты пикселя
	return [i&1 for i in pix]

def set_new_lsb(pix, lsb):
	#возвращает новые цветовые компоненты пикселя такие, чтобы младшие биты были равны lsb
	temp = [i^j for i, j in zip(get_lsb(pix), lsb)]
	temp+=[0]*(3 - len(temp))
	return [(i+flip(i, j)) for i, j in zip(pix, temp)]


def image_to_bin_list(img, n):
	#возвращает вектор из младших битов пикселей изображения длины n, если это возможно
	obj = img.load()
	container = []
	size = min(n, img.size[0]*img.size[1]*3)
	length = min(n//3+n%3-(n%3)//2, img.size[0]*img.size[1])
	for i in range(length):
		container.extend(get_lsb(obj[i%img.size[0], i//img.size[0]]))
	return container

def emb_in_image(img, container, filename_new_image):
	#изменяет младшие биты в изображении так, чтобы вложить сообщение
	length = min(len(container)//3+len(container)%3-(len(container)%3)//2, img.size[0]*img.size[1])
	obj = img.load()
	for i in range(length):
		obj[i%img.size[0], i//img.size[0]]= tuple(set_new_lsb(obj[i%img.size[0], i//img.size[0]], container[i*3:(i+1)*3+len(container)%3]))
	print(filename_new_image)
	img.save(filename_new_image)
	
