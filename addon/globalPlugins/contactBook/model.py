# -*- coding: UTF-8 -*-

# Database modeling.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# Non-standard Python imports from NVDA.
import os
import sys
baseDir = os.path.dirname(__file__)
libs = os.path.join(baseDir, "lib")
sys.path.append(libs)
import sqlite3 as sql

dirDatabase = ""


class ObjectContact(object):

	def __init__(self, id='', name='', cell='', landline='', email=''):
		self.id = id
		self.name = name
		self.cell = cell
		self.landline = landline
		self.email = email

# Returns a formatted string.
	def __repr__(self):
		return ' ' % (self.name, self.cell, self.landline, self.email)

class Section():
	# Import the database path.
	from .configPanel import dirDatabase
	database = dirDatabase
	connect = None
	cursor = None
	connected = False

	# Connect to the database.
	def connection(self):
		Section.connect = sql.connect(Section.database)
		Section.cursor = Section.connect.cursor()
		Section.connected = True

	# Disconnect from the database.
	def disconnect(self):
		Section.connect.close()
		Section.connected = False

# Run "SQL" queries against the database.
	def execute(self, sql, parms=None):
		if Section.connected:
			if parms == None:
				Section.cursor.execute(sql)
			else:
				Section.cursor.execute(sql, parms)
			return True
		else:
			return False

	# Perform one or more INSERT, UPDATE, or DELETE queries.
	def executemany(self, sql, parms=None):
		if Section.connected:
			if parms == None:
				Section.cursor.executemany(sql)
			else:
				Section.cursor.executemany(sql, parms)
			return True
		else:
			return False

# converts the result of a query into a dictionary.
	def dict_factory(cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d

	# retrieve all rows from the result of a query.
	def fetchall(self):
		Section.cursor.row_factory = Section.dict_factory
		return Section.cursor.fetchall()

# commit changes made to a database transaction.
	def persist(self):
		if Section.connected:
			Section.connect.commit()
			return True
		else:
			return False

# Check the existence of the database.
	def initDB():
		trans = Section()
		trans.connection()
		trans.execute(
			"CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY , name TEXT, cell TEXT, landline TEXT, email TEXT)")
		trans.persist()
		trans.disconnect()
