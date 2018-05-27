import os

class Model(object):
	def __init__(self, mode = 0, method = 0, m= 2, decoder = 2):

		"""mode = 0 --вложение
		   mode = 1 -- извлечение
		   method = 0 -- синдромный метод вложения
		   method = 1 -- алфавитный метод вложения
		   m from 2 to 11 -- корректный параметр для синдромного метода
		   m from 2 to 4 -- корректный параметр для алфавитного метода
		   decoder from 0 to 2 -- виды декодера для синдромного метода
		   decoder  = None -- в алфавитном методе не используется декодер
		   message_name -- имя файла с секретным сообщением
		   image_name -- имя файла с изображением
		"""
		self.mode = mode
		self.method = method
		self.decoder = decoder
		self.m = m
		self.image_name =""
		self.message_name = ""
		self._from = 2
		self._to =11


	def is_correct(self):
		if (self.method == 0) and (self.m in range(2,12)) and (self.decoder in range(3)) and os.path.isfile(self.image_name) and os.path.isfile(self.message_name):
			return True
		elif (self.method == 1) and (self.m in range(2,5)) and (self.decoder == None) and os.path.isfile(self.image_name) and os.path.isfile(self.message_name):
			return True
		else:
			return False

	def set_mode(self, mode):
		if (mode in range(2)):
			self.mode = mode

	def set_method(self, method):
		if (method in range(2)):
			self.method = method
			self.m = 2
		else:
			self.method = None
		if self.method == 1:
			self._to = 4
			self.decoder = None
		else:
			 self._to = 11
			 self.decoder = 2


	def set_decoder(self, decoder):
		if self.method == 0: 
			if (decoder in range(3)):
				self.decoder = decoder
			else:
				self.decoder = None

	def set_m(self, m):
		if (self.method == 0) and (m in range(2,12)):
			self.m = m
		elif (self.method == 1) and (m in range(2,5)):
			self.m = m
		else:
			self.m = None

	def set_image_name(self, image_name):
		if os.path.isfile(image_name):
			self.image_name = image_name

	def set_message_name(self, message_name):
		if os.path.isfile(message_name):
			self.message_name = message_name
