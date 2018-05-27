import stego.rm as rm
import stego.wht as wht
"""
	Модуль отвечает за синдромный метод стеганографического вложения.
	Класс Container предназначен для работы с битовыми векторами:
	контейнером и сообщением.
	Имена параметров m,n,r перекочевали сюда из теории кодирования. 
"""
class Container(object):
	def __init__(self, r, m):
		super(Container, self).__init__()
		self.m = m
		self.r = r
		self.check_matrix = rm.make_check_matrix(r,m)
		self.coding_matrix = rm.make_coding_matrix(r,m)
		self.f=[0]*pow(2,m)
		self.message=[]
		self.equation = rm.make_equation(self.check_matrix)
		self.codingWords = rm.make_codewords(self.coding_matrix, self.m)

	def read_container(self, data):
		#считывает новый контейнер
		self.f=list(data)
	
	def get_message(self):
		#извлечение вложенного сообщения из заполненного контейнера
		return rm.compute_sindrom(self.f, self.check_matrix)

	def hide_message(self, mes, mode):
		#вкладывает сообщение в контейнер
		#mode отвечает за модификацию синдромного метода
		self.message=list(mes)
		s=wht.xor(self.message, rm.compute_sindrom(self.f, self.check_matrix))
		if not wht.is_null(s):
			q=rm.solve(self.equation, self.check_matrix, s)
			if(mode == 0):
				e=wht.xor(q,rm.coding(rm.decoder_wht(q),self.coding_matrix))
			elif(mode == 1):
				e = wht.xor(q,rm.brute_force_decoder(q, self.codingWords))
			else:
				e=wht.xor(q,rm.coding(rm.decoderLS(q, self.m),self.coding_matrix))
			g=wht.xor(self.f,e)
			self.f=g	


