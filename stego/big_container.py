from stego.container import Container as ContainerRM
from stego.alp import Container as ContainerAL 

"""
Класс BigContainer предназначен для работы с длинными битовыми векторами:
контейнером и сообщением, которые получены из незначащих битов картинки и 
с помощью перевода текста в битовый вид.
Имена параметров m,n,r перекочевали сюда из теории кодирования. 
"""
class BigContainer(object):
	def __init__(self, r,m, container = [], method = 0):
		self.method = method
		self.n = pow(2, m)

		if self.method ==0:
			self.c = ContainerRM(r,m)
			self.r = self.n-m-1
		else:
			self.c = ContainerAL(m)
			if m==2:
				self.r = 2
			else:
				self.r = self.n-m-1

		self.container = container
		
	def read_container(self, container):
		#считывает новый контейнер
		self.container = container

	def emb(self,message, mode=3):
		#разбивает большой контейнер на части и вызывает соответствующие методы класса контейнер
		full_container = []
		length = min(len(self.container)//self.n, len(message)//self.r)
		for i in range(length):
			self.c.read_container(self.container[i*self.n:(i+1)*self.n])
			self.c.hide_message(message[i*self.r:(i+1)*self.r], mode)
			full_container.extend(self.c.f)
		self.container =  full_container+self.container[len(full_container):len(self.container)]

	def extract(self):
		#извлечение вложенного сообщения из заполненного контейнера
		message=[]
		pos = 0
		for i in range(len(self.container)//self.n):
			self.c.read_container(self.container[i*self.n:(i+1)*self.n])
			message.extend(self.c.get_message())
			if len(message)//8 > pos:
				if message[pos*8:(pos+1)*8] == [1,0,0,1,1,0,0,0]: #стоп-символ
					break
				else:
					pos+=1
		return message
