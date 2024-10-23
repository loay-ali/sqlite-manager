from tkinter import *
from tkinter import filedialog

from sqlite3 import DatabaseError

from inc.db import BWDB

from templates import database as db_template

def choose_db(program):

	try:
		dirname = filedialog.askopenfilename(initialdir = "/",title = "Select DB File")

		#Checks Here
		if dirname == '':
			return

		#Start Connection
		db = BWDB(dirname)

		#Open Window
		db_template.template(program,db)

	except:
		pass

def main():

	window = Tk()
	window.title('SQLite Manager')
	window.geometry('280x200')

	identity_frame = Frame(window)

	Label(identity_frame,text='SQLite Manager',font=('arial',22,'bold'),anchor=CENTER).pack(padx=22,pady=15)

	#Details
	details_frame = Frame(identity_frame)

	#-> Made By
	Label(details_frame,text='By: Loay Ali').grid(row=0,column=0,padx=5,pady=5)

	#-> Version
	Label(details_frame,text='Version: 1.0').grid(row=0,column=1,padx=5,pady=5)

	details_frame.pack()

	identity_frame.grid(row=0,column=0,pady=5,padx=5)

	open_db_btn = Button(window,text='Open DB',width=30,command=lambda: choose_db(window))
	open_db_btn.focus()
	open_db_btn.focus_set()

	open_db_btn.bind('<KeyRelease-Return>',lambda x: choose_db(window))

	open_db_btn.grid(row=1,column=0,padx=5,pady=12)

	close_btn = Button(window,text='Close',width=15,command=lambda: (window.quit(),window.destroy())).grid(row=2,column=0,pady=5,padx=5)

	window.mainloop()

if __name__ == '__main__':
	main()