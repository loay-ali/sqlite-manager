from tkinter import *

def are_you_sure(program,title='Are you sure ?',label='Are you sure ?',confirm=None,deny=None):

	window = Toplevel(program)
	window.title(title)
	window.geometry('150x80')

	Label(window,text=label,anchor=CENTER).grid(row=0,column=0,padx=15,pady=5,columnspan=2)

	Button(window,text='Confirm',command=lambda: (window.destroy(),confirm()) if callable(confirm) else window.destroy()).grid(row=1,column=0,padx=10,pady=5)

	Button(window,text='Cancel',command=lambda: (window.destroy(),deny()) if callable(deny) else window.destroy()).grid(row=1,column=1,padx=10,pady=5)

def info(program,title='Info',label=''):

	window = Toplevel(program)
	window.title(title)
	window.geometry('150x100')

	Label(window,text=label,anchor=CENTER).grid(row=1,column=0,padx=5,pady=5)

	Button(window,text='OK',width=15,anchor=CENTER).grid(row=2,column=0,padx=5,pady=5)