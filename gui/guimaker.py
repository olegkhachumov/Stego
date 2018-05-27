import sys
from tkinter import *
from tkinter.messagebox import showinfo
from gui.sampleedit import SimpleEditor

class GuiMaker(Frame):
	menuBar = []
	toolBar = []
	helpButton = True

	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.parent = parent
		self.pack(expand=YES, fill=BOTH)
		self.start()
		self.makeMenuBar()
		self.makeToolBar()
		self.makeWidgets()

	def makeMenuBar(self):
		menubar = Frame(self, relief=RAISED, bd=2)
		menubar.pack(side=TOP, fill=X)
		for (name, key, items) in self.menuBar:
			mbutton = Menubutton(menubar, text=name, underline=key)
			mbutton.pack(side=LEFT)
			pulldown = Menu(mbutton)
			self.addMenuItems(pulldown, items)
			mbutton.config(menu=pulldown)
		if self.helpButton:
			Button(menubar, text = 'Help',
					cursor='hand2',
					relief = FLAT,
					command = self.help).pack(side=RIGHT)
	

	def addMenuItems(self, menu, items):
		for item in items:
			if item == 'separator':
				menu.add_separator({})
			elif type(item) == list:
				for num in item:
					menu.entryconfig(num, state=DISABLED)
			elif type(item[2]) != list:
				menu.add_command(label = item[0],
								underline = item[1],
								command = item[2])
			else:
				pullover = Menu(menu)
				self.addMenuItems(pullover, item[2])
				menu.add_cascade(label = item[0],
								underline = item[1],
								menu = pullover)

	def makeToolBar(self):
		if self.toolBar:
			toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
			toolbar.pack(side=BOTTOM, fill=X)
			for (name, action, where) in self.toolBar:
				Button(toolbar, text=name, command=action).pack(where)


	def makeWidgets(self):
		pass
		
	def help(self):
		showinfo('Help', 'Sorry, no help for ' + self.__class__.__name__)
	def start(self):
		pass
