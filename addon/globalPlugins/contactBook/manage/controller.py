# -*- coding: UTF-8 -*-

# Control module.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# Standard Python imports.
import os

# Imports from NVDA.
import config

# Non-standard Python imports from NVDA.
from ..lib import sqlite3
from ..lib import csv

from .model import Section, ObjectContact
from ..configPanel import *

# . Function that retrieves all data from the datadataBase.


def get_all_records():
	trans = Section()
	trans.connection()
	trans.execute("SELECT * FROM contacts ORDER BY name ASC")
	results = trans.fetchall()
	rows = convert_results(results)
	trans.disconnect()
	return rows

# Convert results into OlvContact objects.


def convert_results(results):
	print()
	rows = []
	for record in results:
		contact = ObjectContact(
			record['id'], record['name'], record['cell'], record['landline'], record['email'])
		rows.append(contact)
	return rows

# Function to insert new records in the datadataBase.


def add_record(data):
	name = data['contacts']['name']
	cell = data['contacts']['cell']
	landline = data['contacts']['landline']
	email = data['contacts']['email']
	trans = Section()
	trans.connection()
	trans.execute("INSERT INTO contacts VALUES(NULL, ?,?,?,?)",
				  (name, cell, landline, email))
	trans.persist()
	trans.disconnect()

# Search the datadataBase dataBased on the chosen filter and the keyword
# given by the user.


def search_records(filterChoice, keyword):
	trans = Section()
	trans.connection()

	if filterChoice == 'Nome':
		trans.execute("SELECT * FROM contacts WHERE name LIKE ?",
					  ('%' + keyword + '%',))
		results = trans.fetchall()
	elif filterChoice == 'Celular':
		trans.execute("SELECT * FROM contacts WHERE cell LIKE ?",
					  ('%' + keyword + '%',))
		results = trans.fetchall()
	elif filterChoice == 'Telefone fixo':
		trans.execute("SELECT * FROM contacts WHERE landline LIKE ?",
					  ('%' + keyword + '%',))
		results = trans.fetchall()
	elif filterChoice == 'E-mail':
		trans.execute("SELECT * FROM contacts WHERE email LIKE ?",
					  ('%' + keyword + '%',))
		results = trans.fetchall()
	print()
	rows = convert_results(results)
	trans.disconnect()
	return rows

# Function to update records.


def edit_record(ID, row):
	trans = Section()
	trans.connection()
	name = row['name']
	cell = row['cell']
	landline = row['landline']
	email = row['email']
	trans.execute("UPDATE contacts SET name =?, cell=?, landline=?, email=? WHERE id = ?",
				  (name, cell, landline, email, ID))
	trans.persist()
	trans.disconnect()

# Function to remove records.


def delete(id):
	trans = Section()
	trans.connection()
	trans.execute("DELETE FROM contacts WHERE id=?", (id,))
	trans.persist()
	trans.disconnect()


# Delete all records from the datadataBase.
def reset_record():
	trans = Section()
	trans.connection()
	trans.execute("DELETE FROM contacts")
	trans.persist()
	trans.disconnect()

# Importing csv into the datadataBase.


def to_records(mypath):
	trans = Section()
	trans.connection()

	# Opening the csv file.
	with open(mypath, 'r') as file:

		# Extracting the contents of the csv file.
		contents = csv.reader(file, delimiter=',')
		# Writing the data to the database.
		insert_records = "INSERT INTO contacts(name, cell, landline, email) VALUES(?, ?, ?, ?)"
		trans.executemany(insert_records, contents)
	trans.persist()
	trans.disconnect()

# Exporting from the agenda to a csv file.


def to_csv(mypath):
	# connect to the database
	conn = sqlite3.connect(dirDatabase)

	# select data from the contacts table.
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM contacts")

	# write the data to a CSV file
	with open(mypath, "w", newline="") as file:
		newFile = csv.writer(file)

		data = [row for row in cursor]
		result = [[row[i] for i in range(len(row)) if i != 0] for row in data]
		newFile.writerows(result)

# Count the total record registered in the data base.


def count_records():
	trans = Section()
	trans.connection()
	trans.execute("SELECT * FROM contacts")
	result = len(trans.fetchall())
	trans.persist()
	trans.disconnect()
	return result
