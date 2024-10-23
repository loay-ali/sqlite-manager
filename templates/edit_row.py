from tkinter import *

from inc.quick_windows import are_you_sure

def save_data(program,db,table,original_data,data,list):

	if table.update_specific(original_data,data) == True:

		list.item(list.focus(),values=(tuple(data.values())))

		db._connection.commit()
		program.destroy()

def template(program,db,table,data,list):

	window = Toplevel(program)
	window.title('Update Row Data')
	window.geometry('300x400')

	original_data = data.copy()

	toprow = Frame(window)

	Label(toprow,text=db._name +' > '+ table._slug +' > New Row').pack(padx=5,pady=5)

	new_data_frame = Frame(window)

	new_data = Canvas(new_data_frame)
	scroll = Scrollbar(new_data_frame,command=new_data.yview)
	new_data.config(yscrollcommand=scroll.set)

	#Fill Data
	tmp_vars = {}
	for item in table._rows:

		tmp_frame = Frame(new_data)
		tmp_input = None

		Label(tmp_frame,text=item['slug'].capitalize() +' :').pack(side=LEFT,padx=5,pady=5)

		type = item['type'].lower()

		if type == 'text' or type == 'integer' or type == 'real':
			tmp_vars[item['slug']] = Entry(tmp_frame)

			if item['slug'] in data.keys():
				tmp_vars[item['slug']].insert(0,data[item['slug']])

			tmp_vars[item['slug']].pack(side=RIGHT,padx=5,pady=5)

		tmp_frame.pack()

	bottomrow = Frame(window)

	#Insert Data Button
	Button(
		bottomrow,
		text='Save',
		command=lambda: are_you_sure(window,confirm=lambda: save_data(window,db,table,original_data,{
			i['slug']: (("'" if i['type'] == 'text' and tmp_vars[i['slug']].get() != '' else '') + tmp_vars[i['slug']].get() + ("'" if i['type'] == 'text' and tmp_vars[i['slug']].get() != '' else '')) for i in table._rows if i['slug'] in tmp_vars.keys()
		},list))
		).pack(side=LEFT,padx=5,pady=5)
	Button(bottomrow,text='Cancel',command=lambda: window.destroy()).pack(side=RIGHT,padx=5,pady=5)

	#Displaying
	toprow.pack()
	new_data.pack(side=RIGHT,fill=BOTH)
	scroll.pack(side=LEFT,fill=Y,expand=True)
	new_data_frame.pack()
	bottomrow.pack(side=BOTTOM)