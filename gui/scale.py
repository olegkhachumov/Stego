from tkinter import * 

class Scal(Frame):
	def __init__(self, funk, model, parent = None, _text = ""):
		fr = Frame
		fr.__init__(self, parent)
		fr.config(self, bd =5,relief=GROOVE)
		fr.pack(self,fill=X)
		self.parent = parent
		self.model = model
		self.var = IntVar()
		self.scale = Scale(self, from_=self.model._from, to=self.model._to, command=self.onScale, variable=self.var, orient=HORIZONTAL)
		self.scale.pack(side=TOP, padx=15)
		self.funk = funk
		Label(self, text = _text, anchor=CENTER).pack(side=TOP, anchor=N, expand=NO)

	def onScale(self, val):
		#print(val)
		v = int(float(val))
		self.var.set(v)
		self.funk(v)
	def update(self, _to, with_set = False):
		if _to == 0:
			value = 11
		else:
			value = 4
		self.scale.configure( to=value)
		if with_set == True:
			self.var.set(2)

	def bind(self, sequence=None, func=None, add=None):
		for child in self.winfo_children():
			child.bind(sequence, func, add)
			Scal.bind(child, sequence, func, add)
