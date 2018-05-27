from tkinter import *

from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename

from gui.scrolledtext import ScrolledText


class SimpleEditor(ScrolledText): 
	def __init__(self, model, parent=None, file=None):
		frm = Frame(parent)
		frm.pack(fill=X)
		Button(frm, text='Save As', command=self.onSaveAs).pack(side=LEFT)
		Button(frm, text='Save', command=self.onSave).pack(side=LEFT)
		Button(frm, text='Cut', command=self.onCut).pack(side=LEFT)
		Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
		Button(frm, text='Find', command=self.onFind).pack(side=LEFT)
		Button(frm, text='Вложить это сообщение', command=self.choose).pack(side=LEFT)
		self.model = model
		self.file = file
		self.parent=parent
		ScrolledText.__init__(self, parent, file=file)
		self.text.config(font=('courier', 11, 'normal'))
		self.text.bind('<Control-f>', lambda a : self.onFind())


	def choose(self):
		if self.onSave() == 1:
			self.parent.destroy()
		else:
			self.parent.focus()

	def onSave(self):
		if self.file == None:
			return self.onSaveAs()
		else:
			alltext = self.gettext()
			open(self.file, 'w').write(alltext)
			print(self.file)
			self.model.set_message_name(self.file)
			return 1
			self.parent.focus()

	def onSaveAs(self):
		filename = asksaveasfilename( title='Save file',defaultextension=".txt", filetypes = (("text files","*.txt"),("all files","*.*")))
		if filename:
			self.file = filename
			alltext = self.gettext()
			open(filename, 'w').write(alltext)
			print(filename)
			self.model.set_message_name(filename)
			self.parent.focus()
			return 1
		else:
			self.parent.focus()

	def onCut(self):
		text = self.text.get(SEL_FIRST, SEL_LAST)
		self.text.delete(SEL_FIRST, SEL_LAST)
		self.clipboard_clear()
		self.clipboard_append(text)

	def onPaste(self):
		try:
			text = self.selection_get(selection='CLIPBOARD')
			self.text.insert(INSERT, text)
		except TclError:
			pass
	
	def onFind(self):
		target = askstring('SimpleEditor', 'Search String?',parent=self)
		if target:
			where = self.text.search(target, INSERT, END) 
			if where:
				print(where)
				pastit = where + ('+%dc' % len(target))
				self.text.tag_add(SEL, where, pastit) 
				self.text.mark_set(INSERT, pastit) 
				self.text.see(INSERT)
				self.text.focus()
