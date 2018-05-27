from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from gui.scrolledtext import ScrolledText # или tkinter.scrolledtext


class GuiMixin:
	def infobox(self, title, text, *args): # используются стандартные диалоги
		return showinfo(title, text) # *args для обратной совместимости
	
	def errorbox(self, text):
		showerror('Error!', text)
	
	def question(self, title, text, *args):
		return askyesno(title, text) # вернет True или False
	
	def notdone(self):
		showerror('Not implemented', 'Option not available')
	
	def quit(self):
		ans = self.question('Verify quit', 'Are you sure you want to quit?')
		if ans:
			Frame.quit(self) # нерекурсивный вызов quit!
	
	def help(self): # переопределите более
		self.infobox('RTFM', 'See figure 1...') # подходящим
	
	def selectOpenFile(self, file="", dir=".",filetypes=(("all files","*.*"),("all files","*.*"))): # испол-ся стандартные диалоги
		return askopenfilename(initialdir=dir, initialfile=file, filetypes =filetypes)
	
	def selectSaveFile(self, file="", dir="."):
		return asksaveasfilename(initialfile=file, initialdir=dir)
	
	def clone(self, args=()): # необязательные аргументы конструктора
		new = Toplevel() # создать новую версию
		myclass = self.__class__ # объект класса экземпляра (самого низшего)
		myclass(new, *args) # прикрепить экземпляр к новому окну
	

	
	def browser(self, filename, title = "Text Viewer"):
		new = Toplevel() # создать новое окно
		view = ScrolledText(new, file=filename) # Text с полосой прокрутки
		view.text.config(height=30, width=85) # настроить Text во фрейме
		view.text.config(font=('courier', 10, 'normal')) # моноширинный шрифт

		new.title(title) # атрибуты менеджера окон
		#new.iconname("browser") # текст из файла будет
								# вставлен автоматически
		"""
		def browser(self, filename): # на случай, если импортирован
		new = Toplevel() # модуль tkinter.scrolledtext
		text = ScrolledText(new, height=30, width=85)
		text.config(font=('courier', 10, 'normal'))
		text.pack(expand=YES, fill=BOTH)
		new.title("Text Viewer")
		new.iconname("browser")
		text.insert('0.0', open(filename, 'r').read() )
		"""
if __name__ == '__main__':
	class TestMixin(GuiMixin, Frame): # автономный тест
		def __init__(self, parent=None):
			Frame.__init__(self, parent)
			self.pack()

			Button(self, text='quit', command=self.quit).pack(fill=X)
			Button(self, text='help', command=self.help).pack(fill=X)
			Button(self, text='clone', command=self.clone).pack(fill=X)
			Button(self, text='open', command=self.selectOpenFile).pack(fill=X)
	
	TestMixin().mainloop()