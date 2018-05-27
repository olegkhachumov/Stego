import sys
import os
import glob
import time
import multiprocessing	
from tkinter import * 
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo

from gui.guimixin import GuiMixin
from gui.sampleedit import SimpleEditor
from gui.editor import Editor
from gui.scrolledtext import ScrolledText
from gui.guimaker import GuiMaker
from gui.wiewresult import WiewResult
from gui.radiobar import Radiobar
from gui.scale import Scal
from gui.model import Model

import StegoConsole



class myMenu(GuiMixin, GuiMaker):
		def start(self):
			self.menuBar = [
					('Файл', 0,
					[('Выбрать изображение', 0, lambda:self.selectImageFile()),
					('Выбрать сообщение', 0, lambda: self.selectMessageFile()),
					('Создать новое сообщение', 0, lambda: self.selectMessageFile(True)),
					('Выход', 0, sys.exit)])] 
					#('Edit', 0,
					#[('Cut', 0, lambda:0),
					#('Paste', 0, lambda:0)]) ]
			self.toolBar = [('Выход', sys.exit, {'side': LEFT})]
			self.model = Model()


		def help(self):
			self.browser("help.txt", title = "Справка")

		def selectMessageFile(self, empty = False):
			new = Toplevel()
			new.title('Message redactor')
			new.iconname("browser")
			new.withdraw()
			if not empty:
				filename = self.selectOpenFile(filetypes = (("text files","*.txt"),("all files","*.*")))
				if  os.path.isfile(filename):

					new.deiconify()
					view = SimpleEditor(model = self.model, parent = new, file=filename)
					view.text.config(height=30, width=85)
					view.text.config(font=('courier', 10, 'normal'))
			else:
				view = SimpleEditor(model = self.model,parent = new, file = None)
				new.deiconify()
				view.text.config(height=30, width=85)
				view.text.config(font=('courier', 10, 'normal'))

		def selectImageFile(self):
			filename = self.selectOpenFile(filetypes = (("bitmap files","*.bmp"),("bitmap files","*.png"),("all files","*.*")))
			if filename:
				self.model.set_image_name(filename)
				img = Image.open(filename)
				img.save('temp/temp.bmp')
				ratio = (self.canvas_width / float(max(img.size[0], img.size[1])))
				height = int((float(img.size[0]) * float(ratio)))
				width = int((float(img.size[1]) * float(ratio)))

				img = img.resize((height, width), Image.ANTIALIAS)
				self.image = ImageTk.PhotoImage(img)
				self.can.create_image(self.canvas_height//2+5,self.canvas_width//2+5,image=self.image)

		def startEmb(self):
			if self.model.is_correct():
				def exit():
					self.t.terminate()
					self.waitwindow.destroy()
					files = glob.glob('temp/*')
					for f in files:
						if f != 'temp\\temp.bmp':
							os.remove(f)
				self.waitwindow = Toplevel(bg= "gray")
				Label(self.waitwindow, text = "Идет процесс вложения,\nэто может занять некоторое время.", height = 5, width = 50,wraplength = 200,bg= "gray").pack()
				Button(self.waitwindow, text='Отмена', command = exit).pack()
				self.waitwindow.grab_set()
				self.waitwindow.overrideredirect(2)
				w = self.waitwindow.winfo_screenwidth()
				h = self.waitwindow.winfo_screenheight()
				size = (250,150)
				x = w/2 - size[0]/2
				y = h/2 - size[1]/2
				self.waitwindow.geometry("%dx%d+%d+%d" % (size + (x, y)))
				self.waitwindow.protocol('WM_DELETE_WINDOW', exit)
				self.t = multiprocessing.Process(target=StegoConsole.embedding, 
												args=(self.model.m, 
													self.model.image_name, 
													self.model.message_name,"temp/stego.bmp",  
													self.model.decoder, self.model.method))
				self.t.start()
				while self.t.is_alive():
					self.waitwindow.update()
				if os.path.isfile('temp/stego.bmp'):
					tl = Toplevel()
					WiewResult(tl, "temp/temp.bmp", "temp/stego.bmp")
					WiewResult(tl, "temp/temp_rgb_gist.png", "temp/stego_rgb_gist.png")
				self.waitwindow.destroy()
			else:
				showinfo('Ошибка','Не выбрано изображение или сообщение для вложения')

		def startExt(self):
			if os.path.isfile(self.model.image_name):
				def exit():
					self.t.terminate()
					self.waitwindow.destroy()
				self.waitwindow = Toplevel(bg= "gray")
				Label(self.waitwindow, text = "Идет процесс извлечения,\nэто может занять некоторое время.", height = 5, width = 50,wraplength = 200,bg= "gray").pack()
				Button(self.waitwindow, text='Отмена', command = exit).pack()
				self.waitwindow.grab_set()
				self.waitwindow.overrideredirect(2)
				w = self.waitwindow.winfo_screenwidth()
				h = self.waitwindow.winfo_screenheight()
				size = (250,150)
				x = w/2 - size[0]/2
				y = h/2 - size[1]/2
				self.waitwindow.geometry("%dx%d+%d+%d" % (size + (x, y)))
				self.waitwindow.protocol('WM_DELETE_WINDOW', exit)
				self.t = multiprocessing.Process(target=StegoConsole.extract, args=(self.model.m, self.model.image_name, "temp/secret_message.txt", self.model.method))
				self.t.start()
				while self.t.is_alive():
					self.waitwindow.update()
				if os.path.isfile('temp/secret_message.txt'):
					new = Toplevel()
					view = Editor(parent = new, file='temp/secret_message.txt')
					view.text.config(height=30, width=85) 
					view.text.config(font=('courier', 10, 'normal'))
				self.waitwindow.destroy()
			else:
				showinfo('Ошибка','Не выбрано изображение для извлечения')

		def startW(self):
			if self.model.mode==0:
				self.startEmb()
			else:
				self.startExt()

		def makeWidgets(self):
			fr = Frame(self, bd =15)
			rbmode = Radiobar(funk = self.model.set_mode, 
								parent = fr, picks= ['Вложение', 'Извлечение'],
								_text = 'Выберете режим работы',  
								side=TOP, anchor=NW, default_value = 0)
			rbmode.pack(side=TOP,expand=YES, fill = BOTH)
			def update_decoder(mode):
				if mode==1:
					rb2.pack_forget()
					self.message_button.pack_forget()
				else:
					rb2.pack(side=TOP, expand=YES,fill = BOTH)
					self.message_button.pack(fill=None, expand=NO, side=TOP)

			rbmode.bind('<Button-1>',lambda a: update_decoder(self.model.mode))
			rbmode.bind('<Leave>',lambda a:update_decoder(self.model.mode))

			rb1 = Radiobar(funk = self.model.set_method, 
								parent = fr, picks= ['Синдромный метод', 'Алфавитный метод'],
								_text = 'Выберете метод',  
								side=TOP, anchor=NW, default_value = 0)
			rb1.pack(side=TOP,expand=YES, fill = BOTH)
			sca = Scal(funk = self.model.set_m, model = self.model,  parent = fr, _text = "параметр m")
			sca.pack(side=TOP,  expand=YES, fill = BOTH)
			rb2 = Radiobar(funk = self.model.set_decoder, 
							parent = fr, picks=['Декодер БПУ', 'Переборный декодер',  'Декодер Лицына-Шеховцова'],
							_text = 'Выберете декодер', side=TOP, 
							anchor=NW, default_value = 2)
			rb2.pack(side=TOP, expand=YES,fill = BOTH)
			
			def update():
				sca.update(int(rb1.state()), with_set = True)
				rb2.var.set(2)

			rb1.bind('<Button-1>',lambda a: update())
			rb1.bind('<Leave>',lambda a: sca.update(int(rb1.state())))
			fr.pack(expand=NO, fill = Y	, side =LEFT)

			fr1 = Frame(self, bd =15)
			self.fr2 = Frame(fr1, height =700, width = 700, bd = 5,relief=GROOVE)
			
			self.canvas_width=500
			self.canvas_height=500
			self.can = Canvas(self.fr2, width=self.canvas_width,height=self.canvas_height, bd = 5,relief=GROOVE)
			self.can.pack(fill=BOTH, expand=NO, side=TOP) 
			Button(self.fr2, text='СТАРТ', command=self.startW).pack(fill=None, expand=NO, side=TOP)
			Button(self.fr2, text='Выбрать изображение', command=self.selectImageFile).pack(fill=None, expand=NO, side=TOP)
			self.message_button=Button(self.fr2, text='Выбрать сообщение', command=self.selectMessageFile)
			self.message_button.pack(fill=None, expand=NO, side=TOP)			
			
			self.fr2.pack(expand=NO, fill = Y, side = LEFT)

			fr1.pack(expand=NO, fill = Y, side =LEFT)
			


if __name__ == '__main__':
	os.makedirs('temp', mode=0o777, exist_ok=True)
	files = glob.glob('temp/*')
	for f in files:
		os.remove(f)
	root = Tk()
	root.title('Stego')
	root.iconbitmap(default='gui/icon.ico')
	root.geometry("800x800")
	myMenu(root)

	root.mainloop()