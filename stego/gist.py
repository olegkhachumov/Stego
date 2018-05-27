from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np

"""
Модуль преднозначен для создания гистограмм изображения. 
Создает гистограммы красной, синей, зеленой компоненты цвета,
rgb гистограмму и гистограмму яркости.
"""
def make_gist(bins, data, width=1, color = "black", filename_gist=""):
	fig = plt.figure()
	plt.bar(bins,data, width=width, color = color)
	plt.ylabel('Количество')
	plt.xlabel('Значение цвета')
	fig.savefig(filename_gist)
	plt.clf()

def make_all_gist(filename, path=""):
	#создает гистограммы для изображения filename и сохраняет их в папке path
	data= Image.open(filename).histogram()
	bins=[i for i in range(256)]
	width = 1
	make_gist(bins, data[0:256], width=width, color = "red", filename_gist=path+'red_gist.png')
	make_gist(bins, data[256:512], width=width, color = "green", filename_gist=path+'green_gist.png')
	make_gist(bins, data[512:768], width=width, color = "blue", filename_gist=path+'blue_gist.png')
	data1 = [data[i]+data[i+256]+data[i+512] for i in range(256)]
	make_gist(bins, data1, width=width, color = "gray", filename_gist=path+'rgb_gist.png')
	data= Image.open(filename).convert("L").histogram()
	make_gist(bins, data, width=width, color = "gray", filename_gist=path+'gray_gist.png')


