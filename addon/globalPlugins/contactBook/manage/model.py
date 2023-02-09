# -*- coding: UTF-8 -*-

# Database modeling.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# start of the necessary imports for the module to work correctly.
import os
from ..lib import sqlite3 as sql


# Database location.
database = os.path.join(os.path.dirname(__file__), "agenda.db")

class ObjectContact(object):

	def __init__(self, id='', name='', cell='', landline='', email=''):
		self.id = id
		self.name = name
		self.cell = cell
		self.landline = landline
		self.email = email


class Section():
	database = database 
	connect		= None
	cursor		 = None
	connected   = False

	def connection(self):
		Section.connect = sql.connect(Section.database)
		Section.cursor	   = Section.connect.cursor()
		Section.connected = True

	def disconnect(self):
		Section.connect.close()
		Section.connected = False

	def execute(self, sql, parms = None):
		if Section.connected:
			if parms == None:
				Section.cursor.execute(sql)
			else:
				Section.cursor.execute(sql, parms)
			return True
		else:
			return False

	def executemany(self, sql, parms = None):
		if Section.connected:
			if parms == None:
				Section.cursor.executemany(sql)
			else:
				Section.cursor.executemany(sql, parms)
			return True
		else:
			return False

	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	def fetchall(self):
		Section.cursor.row_factory = Section.dict_factory
		return Section.cursor.fetchall()

	def persist(self):
		if Section.connected:
			Section.connect.commit()
			return True
		else:
			return False

	def __repr__(self):
		return ' ' %(self.name, self.cell, self.landline, self.email)

		# Check the existence of the database.
def initDB():
	trans = Section()
	trans.connection()
	trans.execute("CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY , name TEXT, cell TEXT, landline TEXT, email TEXT)")
	trans.persist()
	trans.disconnect()

initDB() # Start the initDB function.
