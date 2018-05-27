from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename
from gui.scrolledtext import ScrolledText 


class Editor(ScrolledText): 
	#класс для отображения извлеченного текстового сообщения из стегоконтейнера
	def __init__(self, parent=None, file=None):
		frm = Frame(parent)
		frm.pack(fill=X)
		Button(frm, text='Save As', command=self.onSaveAs).pack(side=LEFT)
		self.file = file
		self.parent=parent
		ScrolledText.__init__(self, parent, file=file)
		self.text.config(font=('courier', 11, 'normal'))

	def onSaveAs(self):
		filename = asksaveasfilename( title='Save file',defaultextension=".txt", filetypes = (("text files","*.txt"),("all files","*.*")))
		if filename:
			self.file = filename
			alltext = self.gettext() # от начала до конца
			open(filename, 'w').write(alltext) # сохранить текст в файл
		self.parent.focus()

