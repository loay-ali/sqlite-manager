from tkinter import Label,Frame,BooleanVar,NORMAL,DISABLED
from tkinter.ttk import Checkbutton

class BWCheckboxField:

	var = None
	frame = None
	inp = None

	def __init__(self,program,label='',default=False,is_disabled=False):

		self.frame = Frame(program)

		l = self.label(self.frame, label)
		self.inp = self.check(self.frame,default,is_disabled)

		l.bind('<ButtonRelease-1>',lambda x: (self.inp.focus(),self.inp.focus_set()))

		l.grid(row=0,column=0,padx=5,pady=5)
		self.inp.grid(row=0,column=1,padx=5,pady=5)

	def check(self,program,default,is_disabled):

		self.var = BooleanVar(program)
		self.var.set(bool(default))

		return Checkbutton(program,variable=self.var,state=DISABLED if is_disabled == True else NORMAL)

	def label(self,program,title):

		return Label(program,text=title)