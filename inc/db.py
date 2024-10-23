from sqlite3 import DatabaseError,InternalError,NotSupportedError,DataError,OperationalError,ProgrammingError, connect
from re import search
from tkinter import messagebox

from inc.single_table import BWTable
from inc.quick_windows import are_you_sure

def parse_sql_rows(sql):

	sql = sql.split('(')[1]

	return_list = []

	for row in sql.split(','):

		row_data = list(map(lambda ele: ele.lower(),row.strip().split(' ')))

		if len(row_data) < 2:
			continue

		return_list.append({
			'slug': row_data[0],
			'type': row_data[1],
			'key': (row_data[row_data.index('key') - 1] if 'key' in row_data else None),
			'auto_inc': True if 'autoincrement' in row_data else False,
			'default': (row_data[row_data.index('default') + 1] if ('default' in row_data and len(row_data) > row_data.index('default') + 1) else None),
			'is_null': False if ('not' in row_data and 'null' in row_data and row_data.index('not') == (row_data.index('null') - 1)) else True
		})

	return return_list

class BWDB:

	_name = ''

	_cursor = None
	_connection = None

	_tables = []

	def __init__(self,path):

		try:

			#Start Connection
			self._connection = connect(path)
			self._cursor = self._connection.cursor()

			#More Details
			tmp_name = path.split('/')
			self._name = tmp_name[len(tmp_name) - 1]

			#Get Database Structure
			for single_table in  self._cursor.execute("SELECT name,sql FROM sqlite_schema").fetchall():
				tmp_table = BWTable(single_table[0], parse_sql_rows(single_table[1]),self._cursor)
				self._tables.append(tmp_table)

		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
			raise DatabaseError
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
			raise ProgrammingError
		except DataError as err:
			messagebox.showerror('Data Error',err)
			raise DataError
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
			raise OperationalError
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
			raise InternalError
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
			raise NotSupportedError
		except:
			print('DB Init Error')

	def drop_choosed_table(self,table,program):

		choosed = table.focus()

		if choosed == '':
			return

		return self.drop_table(choosed,program)

	def get_table(self,slug):

		for _table in self._tables:

			if _table._slug == slug:
				
				return _table

		return None

	def drop_table(self,slug,program):

		tmp_table = self.get_table(slug)

		if tmp_table == None:
			return False

		#Drop Table From Tables List

		are_you_sure(
			program,
			confirm=lambda: (
				tmp_table.drop(),
				self._connection.commit()))

		return True

	def force_drop_table(self,slug):

		table_obj = self.get_table(slug)

		if table_obj == None:
			return False

		table_obj.drop()

		self._connection.commit()

		return True

	def alter_table(self,table_slug,new_data):

		#Validations
		
		#-> Required Data Existance Check
		new_data_keys = new_data.keys()

		#--> Table Slug
		if 'slug' not in new_data_keys or isinstance(new_data['slug'],str) == False or new_data['slug'] == '':
			return False

		#--> Table Rows
		if 'rows' not in new_data_keys:
			return False

		#Save Table's Data
		table_obj = self.get_table(table_slug)
		tmp_data = table_obj.get()
		tmp_structure = [i['slug'] for i in table_obj._rows]

		list_data = []
		for item in tmp_data:
			list_data.append(
				{tmp_structure[x]: item[x] for x in range(len(tmp_structure))}
			)

		#Drop Table -> Re Create
		if self.force_drop_table(table_slug) == False:
			return False

		if self.new_table(new_data['slug'], new_data['rows']) != True:
			return False

		#Refill Data
		for item in list_data:
			self._tables[-1].insert(item)

		self._connection.commit()

		return True

	def new_table(self,title,table,insert_method=None):

		#Check Title Validate
		#if search('^[a-zA-Z0-9_]$',title) == None:
		#		raise Exception(title='Table Name Is Unvalid ( Only Allowed Characters, Numbers and Underscores )')
		#		return

		rows_data = []

		for item in table.get_children():
			#Check Rows
			#-> Row Slug
			#		if search('^[a-Z0-9_]$',item[0]) == None:
			#			raise Exception(title='Row Name Is Unvalid ( Only Allowed Characters, Numbers and Underscores )')
			#			return

			single_row_data = table.item(item)['values']

			#-> Row Slug Duplicated
			if single_row_data[0] in rows_data:
				raise Exception(title="Row Name Has Been Used Before")
				return

			#Register Data
			rows_data.append({
				'slug': single_row_data[0],
				'type': single_row_data[1].upper(),
				'key': None if single_row_data[2] == None else single_row_data[2].upper(),
				'auto_inc': False if single_row_data[3] in ('✗','-') else True,
				'is_null': False if single_row_data[4] in ('✗','-') else True
			})

		table_obj = BWTable(title, rows_data,self._cursor)
		table_obj.create()
		self._connection.commit()

		self._tables.append(table_obj)

		if insert_method != None:
			insert_method()

		return True

	#Close Connection With Database
	def close(self):

		self._cursor.close()
		self._connection.close()