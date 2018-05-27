import pickle
import math
import stego.wht as wht
import os
"""
	модуль отвечает за метод стеганографического вложения,
	основанный на алфавитном кодировании и преобразовании
	Уолша-Адамара, рассмотренный в магистерской работе.
	Класс Container предназначен для работы с битовыми векторами:
	контейнером и сообщением.
	Имена параметров m,n,r перекочевали сюда из теории кодирования. 

"""


def make_dict(m):
	d = {}
	n=pow(2,m)
	for i in range(0, pow(2,n)):
		f = wht.int_to_list(i, n)
		transform=wht.wht(f)
		transform=wht._abs(transform)
		if tuple(transform) not in d:
			d.update({tuple(transform):[]})
		d[tuple(transform)].append(list.copy(f))
	return d

def make_coding_dict(d, m):
	coding_dict = {}
	n=pow(2,m)
	j = 0;

	if m == 2:
		power=2
	elif m==3:
		power = 4
	elif m== 4:
		power = 11

	kol = pow(2,power)
	for i in d:
		if len(d[i])!=2:
			coding_dict.update({tuple(wht.int_to_list(j, power)):i})
			j+=1
			if j == kol:
				break
		elif m==2:
			coding_dict.update({tuple(wht.int_to_list(j, power)):i})
			j+=1
			if j == kol:
				break
	return coding_dict


def make_decoding_dict(d, m):
	decoding_dict = {}
	n=pow(2,m)
	j = 0;

	if m == 2:
		power=2
	elif m==3:
		power = 4
	elif m== 4:
		power = 11

	kol = pow(2,power)

	for i in d:
		if len(d[i])!=2:
			decoding_dict.update({i:tuple(wht.int_to_list(j, power))})
			j+=1
			if j == kol:
				break
		elif m==2:
			decoding_dict.update({i:tuple(wht.int_to_list(j, power))})
			j+=1
			if j == kol:
				break
	return decoding_dict


def make_prev_dict(m):
	n=pow(2,m)
	prev_dict={}
	prev_dict.update({0:make_dict(m)})
	prev_dict.update({1:make_coding_dict(prev_dict[0], m)})
	prev_dict.update({2:make_decoding_dict(prev_dict[0], m)})
	os.makedirs('stego/dict/', mode=0o777, exist_ok=True)
	with open('stego/dict/'+'dict'+str(m)+'.pickle', 'wb') as file:
		pickle.dump(prev_dict, file)
	return prev_dict


def find_nearest_vector(f, d):
	dist=len(d[0])
	pos=0
	for i in range(len(d)):
		if wht.distance(f,d[i]) < dist:
			dist=wht.distance(f,d[i])
			pos = i
	return d[pos]



class Container(object):
	def __init__(self, m):
		super(Container, self).__init__()
		self.m = m
		self.f=[0]*pow(2,m)
		self.start()
	def start(self):
		#считывает из памяти сгенерированные уже словари или генерирует новые.
		if os.path.isfile('stego/dict/'+'dict'+str(self.m)+'.pickle'):
			with open('stego/dict/'+'dict'+str(self.m)+'.pickle', 'rb') as file:
				data = pickle.load(file)
		else:
			data = make_prev_dict(self.m)
		
		self.dict = data[0]
		self.coding_dict=data[1]
		self.decoding_dict = data[2]

	def read_container(self, data):
		#считывает новый контейнер
		if len(data) == pow(2, self.m):
			self.f=list(data)
	
	def get_message(self):
		#извлекает спрятанное сообщение в f
		if tuple(wht._abs(wht.wht(self.f))) in self.decoding_dict:
			return list(self.decoding_dict[tuple(wht._abs(wht.wht(self.f)))])
		else:
			return []

	def hide_message(self, mes, mode):
		#вкладывает сообщение в контейнер
		self.f = find_nearest_vector(self.f, self.dict[self.coding_dict[tuple(mes)]])

