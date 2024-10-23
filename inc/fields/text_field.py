from tkinter import StringVar,Entry,Label,Frame,DISABLED,NORMAL

class BWTextField:

	var = None
	frame = None
	inp = None

	def __init__(self,program,label='',default_value='',is_disabled=False):

		self.frame = Frame(program)

		l = self.label(self.frame,label)
		self.inp = self.input(self.frame,default_value,is_disabled)
		self.inp.insert(0,default_value)

		l.grid(row=0,column=0,padx=5,pady=5)
		self.inp.grid(row=0,column=1,padx=5,pady=5)

		l.bind('<ButtonRelease-1>',lambda x: (self.inp.focus(),self.inp.focus_set()))

	def set(self,val):

		self.inp.delete(0,10000000)
		self.inp.insert(0,val)
		self.var.set(val)

	def input(self,program,default,is_disabled):

		self.var = StringVar()
		self.var.set(default)

		return Entry(program,textvariable=self.var,state=DISABLED if is_disabled == True else NORMAL)

	def label(self,program,title):

		return Label(program,text=title)