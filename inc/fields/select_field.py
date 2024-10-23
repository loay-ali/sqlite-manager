from tkinter import Label,Frame,StringVar,NORMAL,DISABLED
from tkinter.ttk import Combobox

class BWSelectField:

	var = None
	frame = None
	inp = None

	def __init__(self,program,label='',values=(),default='',is_disabled=False):

		self.frame = Frame(program)

		l = self.label(self.frame, label)
		self.inp = self.select(self.frame,values,default,is_disabled)

		l.bind('<ButtonRelease-1>',lambda x: (self.inp.focus(),self.inp.focus_set()))

		l.grid(row=0,column=0,padx=5,pady=5)
		self.inp.grid(row=0,column=1,padx=5,pady=5)

	def select(self,program,values,default,is_disabled):

		self.var = StringVar(program)

		if default != '':
			self.var.set(default)

		return Combobox(program,values=values,textvariable=self.var,state=DISABLED if is_disabled == True else NORMAL)

	def label(self,program,title):

		return Label(program,text=title)