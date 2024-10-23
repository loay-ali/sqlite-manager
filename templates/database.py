from tkinter import *

from main import main

from templates import table as table_template

from inc.list import BWList
from inc.fields.text_field import BWTextField
from inc.fields.select_field import BWSelectField
from inc.fields.checkbox_field import BWCheckboxField
from inc.quick_windows import are_you_sure

def change_data(col,table,val):

	focus = table.focus()

	if focus == '':
		return

	data = table.item(focus)['values']
	data[col] = val

	table.item(focus,values=(data))

def remove_row(table,to_deactive):

	focus = table.focus()

	if focus == '':
		return

	table.delete(focus)

	for item in to_deactive:
		item.config(state=DISABLED)

def fill_data_on_focus(list,fields):

	choosed = list.list.focus()
	if choosed == '':
		return False

	row = list.list.item(choosed)

	fields['slug'].set(row['values'][0])
	fields['type'].var.set(row['values'][1].capitalize())
	fields['key'].var.set(row['values'][2].capitalize())
	fields['auto_inc'].var.set(True if row['values'][3] == '✓' else False)
	fields['is_null'].var.set(True if row['values'][4] == '✓' else False)

def focus_row(table,to_active,force=False):

	focus = table.focus()

	if force == False and focus == '':
		return

	for item in to_active:
		item.config(state=NORMAL)

	to_active[0].focus_set()
	to_active[0].focus()

def insert_row(table,to_active):

	c = len(table.get_children())

	table.insert('',END,iid=c,text=c,values=('-','-','-','-','-'))

	table.focus_force()
	table.focus()
	table.selection_set([c])
	table.focus_set()

	focus_row(table,to_active,True)

def new_table(program,db,list):

	window = Toplevel(program)

	window.title('New Table')
	window.geometry('645x375')

	tmp_data = {
		'name': '',
		'cols': {}
	}

	LeftFrame = Frame(window)

	#Where Am I
	Label(LeftFrame,text=db._name +' > New Table').grid(row=0,column=0,padx=5,pady=5)

	#New Table's Name
	table_name = BWTextField(LeftFrame,'Table Name')

	#Table's Rows
	table_rows = BWList(
		LeftFrame,
		{
			'slug': {'title': 'Title','width': 100},
			'type': {'title': 'Type','width': 75},
			'key': {'title': 'Key','width': 75},
			'auto_inc': {'title': 'AI','width': 40},
			'is_null': {'title': 'Nullable','width': 60}
		},
		False,
		[])

	rows_operations = Frame(LeftFrame)

	new_rows = Button(rows_operations,text='New')
	remove_rows = Button(rows_operations,text='Remove',state=DISABLED)
	remove_rows.config(command=lambda: remove_row(table_rows.list,remove_rows))

	RightFrame = Frame(window)

	#Row Data Title
	Label(RightFrame,text='Row\'s Data',anchor=CENTER).grid(row=0,column=0,padx=5,pady=5)

	slug = BWTextField(RightFrame,'Slug','',True)
	slug.inp.bind('<KeyRelease>',lambda x: change_data(0,table_rows.list,slug.inp.get()))

	type = BWSelectField(RightFrame,'Type',('Text','Integer','Real','DateTime'),'',True)
	type.inp.bind('<<ComboboxSelected>>',lambda x: change_data(1,table_rows.list,type.var.get()))

	key = BWSelectField(RightFrame,'Key',('None','Primary','Unique','Index'),'',True)
	key.inp.bind('<<ComboboxSelected>>',lambda x: change_data(2,table_rows.list,key.var.get()))

	auto_inc = BWCheckboxField(RightFrame,'Auto Increment',False,True)
	auto_inc.inp.bind('<ButtonRelease-1>',lambda x: (print(auto_inc.var.get()),change_data(3,table_rows.list,'✗' if auto_inc.var.get() == True else '✓')))

	is_null = BWCheckboxField(RightFrame,'Is Null ?',False,True)
	is_null.inp.bind('<ButtonRelease-1>',lambda x: change_data(4,table_rows.list,'✗' if is_null.var.get() == True else '✓'))

	table_rows.list.bind(
		'<ButtonRelease-1>',
		lambda x: (
			remove_rows.config(state=NORMAL),
			focus_row(table_rows.list,(slug.inp,type.inp,key.inp,auto_inc.inp,is_null.inp)),
			fill_data_on_focus(table_rows,{'slug': slug,'type': type,'key': key,'auto_inc': auto_inc,'is_null': is_null})
			))
	new_rows.config(command=lambda: insert_row(table_rows.list,(slug.inp,type.inp,key.inp,auto_inc.inp,is_null.inp)))

	#Save Table Button
	save_all = Button(
		RightFrame,
		text='Save Table',
		command=lambda: are_you_sure(
			window,
			confirm=lambda: (
				db.new_table(table_name.inp.get(),table_rows.list),
				list.list.insert('',END,iid=table_name.inp.get(),values=(table_name.inp.get())),
				window.destroy())))

	#Gridding
	table_name.frame.grid(row=1,column=0,padx=5,pady=5)
	table_rows.top_frame.grid(row=2,column=0,padx=5,pady=5)
	new_rows.grid(row=0,column=0,padx=5,pady=5)
	remove_rows.grid(row=0,column=1,padx=5,pady=5)
	rows_operations.grid(row=3,column=0,padx=5,pady=5)

	LeftFrame.grid(row=0,column=0,padx=5,pady=5)
	slug.frame.grid(row=1,column=0,padx=5,pady=5)
	type.frame.grid(row=2,column=0,padx=5,pady=5)
	key.frame.grid(row=3,column=0,padx=5,pady=5)
	auto_inc.frame.grid(row=4,column=0,padx=5,pady=5)
	is_null.frame.grid(row=5,column=0,padx=5,pady=5)

	save_all.grid(row=6,column=0,padx=5,pady=5)
	RightFrame.grid(row=0,column=1,padx=5,pady=5)

def alter_table_window(program,list,db):

	choosed_table = list.list.focus()
	if choosed_table == '':
		return

	table_obj = db.get_table(choosed_table)
	if table_obj == None:
		return

	window = Toplevel(program)

	window.title('Alter Table')
	window.geometry('645x375')

	LeftFrame = Frame(window)

	#Where Am I
	Label(LeftFrame,text=db._name +' > Alter '+ table_obj._slug +' Table').grid(row=0,column=0,padx=5,pady=5)

	#New Table's Name
	table_name = BWTextField(LeftFrame,'Table Name',table_obj._slug)

	#Table's Rows
	table_rows = BWList(
		LeftFrame,
		{
			'slug': {'title': 'Title','width': 100},
			'type': {'title': 'Type','width': 75},
			'key': {'title': 'Key','width': 75},
			'auto_inc': {'title': 'AI','width': 40},
			'is_null': {'title': 'Nullable','width': 60}
		},
		False,
		[[i['slug'],i['type'],i['key'],'✓' if i['auto_inc'] == True else '✗','✓' if i['is_null'] == True else '✗'] for i in table_obj._rows])

	rows_operations = Frame(LeftFrame)

	new_rows = Button(rows_operations,text='New')
	remove_rows = Button(rows_operations,text='Remove',state=DISABLED)
	remove_rows.config(command=lambda: remove_row(table_rows.list,remove_rows))

	RightFrame = Frame(window)

	#Row Data Title
	Label(RightFrame,text='Row\'s Data',anchor=CENTER).grid(row=0,column=0,padx=5,pady=5)

	slug = BWTextField(RightFrame,'Slug','',True)
	slug.inp.bind('<KeyRelease>',lambda x: change_data(0,table_rows.list,slug.inp.get()))

	type = BWSelectField(RightFrame,'Type',('Text','Integer','Real','DateTime'),'',True)
	type.inp.bind('<<ComboboxSelected>>',lambda x: change_data(1,table_rows.list,type.var.get()))

	key = BWSelectField(RightFrame,'Key',('None','Primary','Unique','Index'),'',True)
	key.inp.bind('<<ComboboxSelected>>',lambda x: change_data(2,table_rows.list,key.var.get()))

	auto_inc = BWCheckboxField(RightFrame,'Auto Increment',False,True)
	auto_inc.inp.bind('<ButtonRelease-1>',lambda x: (print(auto_inc.var.get()),change_data(3,table_rows.list,'✗' if auto_inc.var.get() == True else '✓')))

	is_null = BWCheckboxField(RightFrame,'Is Null ?',False,True)
	is_null.inp.bind('<ButtonRelease-1>',lambda x: change_data(4,table_rows.list,'✗' if is_null.var.get() == True else '✓'))

	table_rows.list.bind(
		'<ButtonRelease-1>',
		lambda x: (
			remove_rows.config(state=NORMAL),
			focus_row(table_rows.list,(slug.inp,type.inp,key.inp,auto_inc.inp,is_null.inp)),
			fill_data_on_focus(table_rows,{'slug': slug,'type': type,'key': key,'auto_inc': auto_inc,'is_null': is_null})
			))
	new_rows.config(command=lambda: insert_row(table_rows.list,(slug.inp,type.inp,key.inp,auto_inc.inp,is_null.inp)))

	#Save Table Button
	save_all = Button(
		RightFrame,
		text='Alter Table',
		command=lambda: are_you_sure(window,confirm=lambda: (db.alter_table(choosed_table,{'slug': table_name.inp.get(),'rows': table_rows.list}),window.destroy())))

	#Gridding
	table_name.frame.grid(row=1,column=0,padx=5,pady=5)
	table_rows.top_frame.grid(row=2,column=0,padx=5,pady=5)
	new_rows.grid(row=0,column=0,padx=5,pady=5)
	remove_rows.grid(row=0,column=1,padx=5,pady=5)
	rows_operations.grid(row=3,column=0,padx=5,pady=5)

	LeftFrame.grid(row=0,column=0,padx=5,pady=5)
	slug.frame.grid(row=1,column=0,padx=5,pady=5)
	type.frame.grid(row=2,column=0,padx=5,pady=5)
	key.frame.grid(row=3,column=0,padx=5,pady=5)
	auto_inc.frame.grid(row=4,column=0,padx=5,pady=5)
	is_null.frame.grid(row=5,column=0,padx=5,pady=5)

	save_all.grid(row=6,column=0,padx=5,pady=5)
	RightFrame.grid(row=0,column=1,padx=5,pady=5)

def fill_rows(table,data):

	for row in table.get_children():
		table.delete(row)

	c = 1
	for item in data:
		table.insert('',END,iid=c,text=c,values=(item['slug'],item['type']))
		c += 1

def view_table_window(program,db,table):

	choosed = table.focus()
	if choosed == '':
		return False

	tmp_table = [i for i in db._tables if i._slug == choosed]

	if len(tmp_table) == 0:
		return False

	table_template.template(program,db,tmp_table[0])

def on_choose_table(db,table,to_active,rows_table):

	choosed = table.focus()

	if choosed == '':
		return

	tmp_rows = [i for i in db._tables if i._slug == choosed]
	if len(tmp_rows) == 0:
		return

	fill_rows(rows_table,tmp_rows[0]._rows)

	#Activate Only On Choose Elements
	for item in to_active:
		item.config(state=NORMAL)

def template(program,db):

	window = Tk()

	window.title('Database Window')
	window.geometry('600x425')

	toprow = Frame(window)

	#Title
	Label(toprow,text='Manage '+ db._name).grid(row=0,column=0,padx=5,pady=5)

	#Get Back ( Close Connection )
	Button(toprow,text='Close DB',command=lambda: (db.close(),window.destroy())).grid(row=0,column=1,padx=2,pady=5)

	toprow.grid(row=0,column=0,padx=5,pady=5)

	LeftFrame = Frame(window)

	content = Frame(LeftFrame)

	#Tables List
	tables_list = BWList(
		LeftFrame,
		{'title': {'title': 'Table'}},
		True,
		list(map(lambda ele: ele._slug,db._tables)))

	tables_operations = Frame(LeftFrame)

	RightFrame = Frame(window)

	rows_list = BWList(
		RightFrame,
		{
			'slug': {'title': 'Slug'},
			'type': {'title': 'Type'}
		},
		True)

	new_table_btn = Button(tables_operations,text='New',command=lambda: new_table(window,db,tables_list))
	remove_table_btn = Button(tables_operations,text='Drop',state=DISABLED,command=lambda: (db.drop_choosed_table(tables_list.list,window),tables_list.delete_choosed(),rows_list.clear()))
	edit_table_btn = Button(tables_operations,text='Alter',state=DISABLED,command=lambda: alter_table_window(window,tables_list,db))
	view_table_btn = Button(tables_operations,text='View',state=DISABLED,command=lambda: view_table_window(window,db,tables_list.list))

	tables_list.list.bind('<ButtonRelease-1>', lambda x: on_choose_table(db,tables_list.list,[remove_table_btn,edit_table_btn,view_table_btn],rows_list.list))

	tables_list.top_frame.grid(row=0,column=0,padx=5,pady=5)
	content.grid(row=0,column=0,padx=5,pady=5)

	new_table_btn.grid(row=0,column=0,padx=5,pady=5)
	remove_table_btn.grid(row=0,column=1,padx=5,pady=5)
	edit_table_btn.grid(row=0,column=2,padx=5,pady=5)
	view_table_btn.grid(row=0,column=3,padx=5,pady=5)

	tables_operations.grid(row=1,column=0,padx=5,pady=5)
	LeftFrame.grid(row=1,column=0,padx=5,pady=5)
	rows_list.top_frame.grid(row=0,column=0,padx=5,pady=5)
	RightFrame.grid(row=1,column=1,padx=5,pady=5)

	#program.quit()
	#program.destroy()

	window.mainloop()