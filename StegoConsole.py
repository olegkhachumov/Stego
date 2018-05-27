from PIL import Image, ImageDraw
import sys
import os
import time
import random
import stego.wht as wht
from stego.big_container import BigContainer
import stego.image_processing as im
import stego.gist as gist

def message_to_bin_list(filename):
	binMessage=[]
	f=open(filename, 'r')
	s=f.read().encode('cp1251')
	for i in s:
		binMessage.extend(wht.int_to_list(i, 8))
	return binMessage


def embedding(m, filename_image, filename_message, filename_new_image = "stego.bmp",  mode = 3,method = 0):
	
	message = message_to_bin_list(filename_message)
	img = Image.open(filename_image)
	n = pow(2,m)
	k = m+1
	if method == 0:
		r = n-k
	else:
		if m ==2:
			r = 2
		else:
			r = n-k

	possible_len_of_message = img.size[0]*img.size[1]*3//n - 8//r - 1
	if possible_len_of_message>0:
		if len(message) <= possible_len_of_message*r:
			message.extend([1,0,0,1,1,0,0,0])
		else:
			message = message[0:possible_len_of_message*r]
			message.extend([1,0,0,1,1,0,0,0])

		if len(message)%r !=0:
			message.extend([0 for i in range(r - len(message)%r)])
		len_of_container = n*(len(message)+1)//r

		container = im.image_to_bin_list(img, len_of_container)

		bc = BigContainer(1, m, container, method= method)
		bc.emb(message, mode)
	
		im.emb_in_image(img, bc.container, filename_new_image)
		os.makedirs('temp', mode=0o777, exist_ok=True)
		if os.path.isfile('temp/stego.bmp'):
			gist.make_all_gist('temp/temp.bmp', path="temp/temp_")
			gist.make_all_gist('temp/stego.bmp', path="temp/stego_")
	else:
		print("Невозможно вложить сообщение, так как изображение слишком маленькое")


def extract(m, filename_image = "stego.bmp", filename_message = "secret_message.txt", method = 0):
	img = Image.open(filename_image) 
	container = im.image_to_bin_list(img, img.size[0]*img.size[1]*3)
	img.close()
	bc = BigContainer(1, m, container, method = method)
	sindrom = bc.extract()
	len_of_message=len(sindrom)//8 - 1

	message=[]
	for i in range(len_of_message):
		if sindrom[i*8:(i+1)*8] == [1,0,0,1,1,0,0,0]:
			break
		else: 
			message.append(wht.list_to_int(sindrom[i*8:(i+1)*8]))
	s=bytearray(message)
	s1=s.decode('cp1251')
	#print(message)
	file = open(filename_message, "w")
	file.write(s1)
	file.close()


if __name__ == '__main__':
	try:
		if sys.argv[1] == '-emb':

			embedding(m = int(sys.argv[2]), 
					filename_image=sys.argv[3], 
					filename_message = sys.argv[4],
					filename_new_image = sys.argv[5],
					mode = int(sys.argv[6]),
					method = int(sys.argv[7]))

		elif sys.argv[1] == '-ext':
			extract(m = int(sys.argv[2]), 
					filename_image=sys.argv[3], 
					filename_message = sys.argv[4],
					method = int(sys.argv[5]))

		elif sys.argv[1] == '-help':
			f = open("help/consolehelp.txt", "r")
			s = f.read()
			f.close()
			print(s)

		else:
			print("Неверно указаны параметры для запуска приложения.\nИспользуйте команду -help")
	except Exception:
				print("Неверно указаны параметры для запуска приложения.\nИспользуйте команду -help")