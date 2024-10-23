from tkinter import *
from tkinter import ttk

class BWList:

	top_frame = None
	list = None

	headings = []

	current_order = ''

	list_data = []

	def clear(self):

		for item in self.list.get_children():
			self.list.delete(item)

		return True

	def delete_choosed(self):

		choosed = self.list.focus()
		if choosed == '':
			return False

		self.list.delete(choosed)

		return True

	def sort(self,orderby = '#',order='ASC'):

		self.current_order = order

		order = order.upper() if (order.upper() in ('DESC','ASC')) else 'ASC'

		tmp_data = self.list_data.copy()

		tmp_data.sort(key=lambda a: a[self.headings.index(orderby) - 1],reverse=True if order == 'DESC' else False)

		self.fill(tmp_data)

	def search(self,keyword):

		self.fill(list(filter(lambda ele: ele.find(keyword) != -1,self.list_data)))

	def fill(self,data):

		for row in self.list.get_children():

			self.list.delete(row)

		c = 1
		for d in data:
			self.list.insert('',END,iid=d,text=str(c),values=d)
			c += 1

	### program -> Parent Window
	### Columns -> {slug: {title: <String>,width: <integer>}}
	### Search  -> Whether To Include Search Field
	### Init Data -> Initial Data To Start With
	def __init__(self,program,columns={},search=False,init_data=[],sort={},horizontal_scroll=False):

		if len(columns) == 0:
			return False

		self.top_frame = Frame(program)

		list_frame = Frame(self.top_frame)

		self.list = ttk.Treeview(list_frame,columns=list(columns.keys()),)

		scrollbar = ttk.Scrollbar(list_frame,command=self.list.yview)
		self.list.config(yscrollcommand=scrollbar.set)

		self.list.column('#0',width=15,anchor=CENTER)
		self.list.heading('#0',text='#')

		enable_sort = False if len(sort) == 0 else True
		sort_keys = sort.keys()
		tmp = []

		columns_keys = columns.keys()
		self.headings = list(columns_keys)

		for c in columns_keys:
			
			self.list.column(c,width=columns[c]['width'] if 'width' in columns[c].keys() else 150,anchor=CENTER)
			self.list.heading(
				c,
				text=columns[c]['title'],
				command=lambda col=c: self.sort(col,'ASC' if (self.current_order == '' or self.current_order == 'DESC') else 'DESC') if enable_sort and c in sort_keys else None)

		top_row = Frame(self.top_frame)

		if search == True:
			Label(top_row,text='Search: ').pack(padx=5,pady=5,side=LEFT)

			search_var = StringVar()
			search_input = Entry(top_row,textvariable=search_var)

			search_input.bind('<KeyRelease>',lambda x: self.search(search_var.get()))
			search_input.pack(padx=5,pady=5,side=LEFT)

		top_row.pack(padx=5,pady=5)

		#Fill Initial Data
		self.list_data = init_data
		self.fill(init_data)

		if horizontal_scroll == True:
			v_scrollbar = ttk.Scrollbar(list_frame,command=self.list.xview,orient='horizontal')
			self.list.config(xscrollcommand=v_scrollbar.set)
			v_scrollbar.pack(side=BOTTOM,fill=X)

		self.list.pack(side=LEFT,fill=X)
		scrollbar.pack(side=RIGHT,expand=True,fill=Y)

		list_frame.pack(padx=5,pady=5)