from tkinter import *

from inc.list import BWList
from inc.quick_windows import are_you_sure

from templates import new_row,edit_row

def update_row(program,db,table,list):

	choosed = list.focus()
	if choosed == '':
		return False

	edit_row.template(program, db, table, dict(zip(list['columns'],list.item(choosed)['values'])),list)

def add_new_row(program,db,table,list):

	new_row.template(program, db, table, list)

def remove_data(db,table,table_list):

	choosed = table_list.focus()
	if choosed == '':
		return False

	table.delete_specific(dict(zip(table_list['columns'],table_list.item(choosed)['values'])))
	db._connection.commit()

	table_list.delete(choosed)

	return True

def choose_row(table,to_activate):

	choosed = table.focus()
	if choosed == '':
		return

	for item in to_activate:
		item.config(state=NORMAL)

def template(program,db,table):

	window = Toplevel(program)

	window.title('Table Window')
	window.geometry('350x425')

	toprow = Frame(window)
	Label(toprow,text=db._name +' > '+ table._slug).grid(row=0,column=0,padx=5,pady=5)

	table_list = BWList(
		window,
		{i['slug']: {'title': i['slug'].capitalize(),'width': 100} for i in table._rows},
		True,
		table.get(),
		{i['slug']: {'slug': i['slug'],'type': i['type']} for i in table._rows},
		True)

	operations_row = Frame(window)

	add_row = Button(operations_row,text='Add',command=lambda: add_new_row(window,db,table,table_list))	
	edit_row = Button(operations_row,text='Edit',command=lambda: update_row(window,db,table,table_list.list),state=DISABLED)	
	remove_row = Button(operations_row,text='Delete',command=lambda: are_you_sure(window,confirm=lambda: remove_data(db,table,table_list.list)),state=DISABLED)	

	table_list.list.bind('<ButtonRelease-1>',lambda x: choose_row( table_list.list,(edit_row,remove_row) ))

	#Gridding
	toprow.pack(padx=5,pady=5)
	table_list.top_frame.pack(padx=5,pady=5)

	add_row.grid(row=0,column=0,padx=5,pady=5)
	edit_row.grid(row=0,column=1,padx=5,pady=5)
	remove_row.grid(row=0,column=2,padx=5,pady=5)

	operations_row.pack(padx=5,pady=5)