from tkinter import * 

class RadiobarBase(Frame):
	def __init__(self, parent=None,  picks=[], _text = '', side=TOP, anchor=NW):
		fr = Frame
		fr.__init__(self, parent)
		fr.config(self,  bd =5,relief=GROOVE)
		fr.pack(self,fill=Y)
		self.var = IntVar()
		self.var.set(0)
		Label(self, text = _text, anchor=CENTER).pack(side=TOP, anchor=N, expand=NO)
		i = 0
		for pick in picks:
			self.rad = Radiobutton(self, text=pick, value=i, variable=self.var,command=self.onPress)
			self.rad.pack(side=side, anchor=anchor, expand=NO)
			i+=1

	def state(self):
		return self.var.get()

	def onPress(self):
		print('result:', self.state())


class Radiobar(RadiobarBase):
	def __init__(self, funk, parent=None,  picks=[], _text = '', side=TOP, anchor=NW, default_value = 0):
		RadiobarBase.__init__(self, parent=parent,  picks=picks, _text = _text, side=side, anchor=anchor)
		self.funk = funk
		self.var.set(default_value)

	def onPress(self):
		#print('result:', self.state())
		self.funk(self.state())
		return self.state()

	def bind(self, sequence=None, func=None, add=None):
		for child in self.winfo_children():
			child.bind(sequence, func, add)
			Radiobar.bind(child, sequence, func, add)

