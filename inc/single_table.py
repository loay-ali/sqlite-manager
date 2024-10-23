from sqlite3 import DatabaseError,ProgrammingError,DataError,OperationalError,InternalError,NotSupportedError
from tkinter import messagebox

class BWTable:

	_slug=''
	_rows=''
	_cursor=None

	def __init__(self,slug,rows,cursor=None):

		self._slug=slug
		self._rows=rows

		self._cursor=cursor

	def delete_specific(self,search):

		if self._cursor == None:
			return False

		try:
			self._cursor.execute("DELETE FROM "+ self._slug +" WHERE "+ (" AND ".join([str(i[0]) +' = '+ ("'" if isinstance(i[1], str) else '')+ str(i[1]) +("'" if isinstance(i[1], str) else '') for i in search.items()])))
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

	def delete(self,search_for,search_value):

		if self._cursor == None:
			return False

		try:
			self._cursor.execute("DELETE FROM "+ self._slug +" WHERE "+ search_for +' = '+ search_value)
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

		return True
	
	def update_specific(self,original_data,data):

		if self._cursor == None:
			return False

		try:
			self._cursor.execute(
				"UPDATE "+ self._slug +" SET "+ (",".join([str(i[0]) +' = '+ ("'" if (isinstance(i[1],str) == True and i[1].isalpha()) else '') + str(i[1]) + ("'" if (isinstance(i[1],str) == True and i[1].isalpha()) else '') for i in data.items()]) +' WHERE '+ (" AND ".join([str(i[0]) +' = '+ ("'" if (isinstance(i[1],str) == True and i[1].isalpha()) else '') + str(i[1]) + ("'" if (isinstance(i[1],str) == True and i[1].isalpha()) else '') for i in original_data.items()]))))
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

		return True		

	def update(self,id,data):

		if self._cursor == None:
			return False

		try:
			self._cursor.execute("UPDATE "+ self._slug +" SET "+ (" AND ".join([str(i[0]) +' = '+ ("'" if isinstance(i[1],str) else '') + str(i[1]) + ("'" if isinstance(i[1],str) else '') for i in data.items()]) +' WHERE id = '+ str(id)))
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

		return True

	def insert(self,data):

		if self._cursor == None:
			return False

		try:
			self._cursor.execute("INSERT INTO "+ self._slug +" ("+ ",".join(list(map(lambda ele: str(ele),list(filter(lambda ele,list=data: list[ele] != '',data.keys()))))) +") VALUES ("+ ",".join(list(map(lambda ele: str(ele),list(filter(lambda ele: ele != '',data.values()))))) +")")
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

		return True

	def get(self,search = {},sort={}):

		if self._cursor == None:
			return []

		search_query = []
		for s in search.keys():
			search_value = ('LIKE %'+ search[s]['value'] +'%') if (search[s]['relation'] == 'LIKE') else ('= '+ search[s]['value'])
			search_query.append(search[s]['slug'] +' '+ search_value)
			
		try:
			res = self._cursor.execute("SELECT * FROM "+ self._slug +(' WHERE ' if len(search_query) != 0 else '')+ (' AND '.join(search_query))).fetchall()
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

		return res

	def create(self):

		rows_str = []
		special_keys = []

		for col in self._rows:
			rows_str.append(col['slug'] +' '+ col['type'] +' '+ ((col['key'] + ' KEY') if col['key'] not in (None,'INDEX','UNIQUE') else '') +' '+ ('AUTOINCREMENT' if col['auto_inc'] == True else '') +' '+ ('NOT NULL' if col['is_null'] == False else ''))

			if col['key'] in ('INDEX','UNIQUE'):
				special_keys.append("CREATE "+ ("UNIQUE" if col['key'] == 'UNIQUE' else '') +' INDEX '+ col['slug'] +'_index ON '+ self._slug +'('+ col['slug'] +')')

		try:
			self._cursor.execute("CREATE TABLE "+ self._slug +" ("+ (','.join(rows_str)) +")")

			for key_statement in special_keys:
				self._cursor.execute(key_statement)
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False

		return True

	def drop(self):

		try:
			self._cursor.execute("DROP TABLE "+ self._slug)
		except DatabaseError as err:
			messagebox.showerror('Database Error',err)
		except ProgrammingError as err:
			messagebox.showerror('Programming Error',err)
		except DataError as err:
			messagebox.showerror('Data Error',err)
		except OperationalError as err:
			messagebox.showerror('Operational Error',err)
		except InternalError as err:
			messagebox.showerror('Internal Error',err)
		except NotSupportedError as err:
			messagebox.showerror('Not Supported Error',err)
		except:
			return False