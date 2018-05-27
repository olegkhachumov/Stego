from tkinter import * 
from PIL import ImageTk, Image


def crop_image(filename, _width):
	img = Image.open(filename)
	ratio = (_width / float(max(img.size[0], img.size[1])))
	height = int((float(img.size[0]) * float(ratio)))
	width = int((float(img.size[1]) * float(ratio)))
	img = img.resize((height, width), Image.ANTIALIAS)
	return ImageTk.PhotoImage(img)
	

class WiewResult(Frame):
	def __init__(self, parent=None, filename_image1="", filename_image2=""):
		Frame.__init__(self, parent)
		self.fr2 = Frame(parent, height =800, width = 800, bd = 5,relief=GROOVE)
		self.canvas_width=400
		self.canvas_height=400

		fr = Frame(self.fr2)
		Label(fr, text = 'Оригинал', anchor=CENTER).pack(side=LEFT, anchor=N, expand=YES)
		Label(fr, text = 'Стего', anchor=CENTER).pack(side=LEFT, anchor=N, expand=YES)
		fr.pack(expand=NO, fill = X, side = TOP)

		self.can1 = Canvas(self.fr2, width=self.canvas_width,height=self.canvas_height, bd = 5,relief=GROOVE)
		self.image1=crop_image(filename_image1, self.canvas_width-10)
		self.can1.create_image(self.canvas_height//2+5,self.canvas_width//2+5,image=self.image1)
		self.can1.pack(fill=BOTH, expand=NO, side=LEFT)

		self.can2 = Canvas(self.fr2, width=self.canvas_width,height=self.canvas_height, bd = 5,relief=GROOVE)
		self.image2=crop_image(filename_image2, self.canvas_width-10)
		self.can2.create_image(self.canvas_height//2+5,self.canvas_width//2+5,image=self.image2)
		self.can2.pack(fill=BOTH, expand=NO, side=LEFT) 

		self.fr2.pack(expand=NO, fill = None, side = TOP)
