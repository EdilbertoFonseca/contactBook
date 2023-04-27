# -*- coding: UTF-8 -*-

# Lists all contacts registered in the phonebook.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# Standard Python imports.
import os

# Standard NVDA imports.
import addonHandler
import gui
import ui
import config
import wx

# non-standard Python imports from NVDA.
from .lib import csv
from .lib.ObjectListView import ObjectListView, ColumnDefn

# imports from the Contact Book addon.
from .addEditRecord import AddEditRecDialog
from .manage import controller as core

# For translation process
addonHandler.initTranslation()


class ContactList(wx.Dialog):

	def __init__(self, parent, title):
		# Title of contact list dialog.
		self.title = title
		try:
			self.contactResults = core.get_all_records()
		except:
			self.contactResults = []

		super(ContactList, self).__init__(parent, title=title)

		# Creating the screen objects.
		panel = wx.Panel(self)
		self.contactList = ObjectListView(
			panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.contactList.SetFocus()
		self.contactList.SetEmptyListMsg(_('No records found!'))
		self.set_contacts()

		labelSearch = wx.StaticText(panel, label=_('Search for: '))
		# List of combobox choices option.
		listOfOptions = [_('Name'), _('Cell phone'), _('Landline'), _('Email')]
		self.comboboxOptions = wx.ComboBox(
			panel, value=_('Name'), choices=listOfOptions)
		self.search = wx.SearchCtrl(panel, -1)
		self.buttonSearch = wx.Button(panel, label=_('&Search'))

		self.buttonEdit = wx.Button(panel, wx.ID_EDIT, label=_('&Edit'))
		self.buttonNew = wx.Button(panel, wx.ID_NEW, label=_('&New'))
		self.buttonDelete = wx.Button(panel, wx.ID_DELETE, label=_('&Remove'))
		self.buttonRefresh = wx.Button(panel, -1, label=_('Refres&h'))
		self.buttonImport = wx.Button(
			panel, wx.ID_DELETE, label=_('&Import csv...'))
		self.buttonExport = wx.Button(
			panel, wx.ID_DELETE, label=_('Ex&port csv...'))
		self.buttonResetRecords = wx.Button(
			panel, -1, label=_('&Delete all records.'))
		self.buttonExit = wx.Button(panel, wx.ID_CANCEL, label=_('E&xit'))
		self.set_config()

		# Creating the layout and adding it to the panel.
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		viewSizer = wx.BoxSizer(wx.HORIZONTAL)
		searchSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

		viewSizer.Add(self.contactList, 0, wx.ALL | wx.EXPAND, 5)
		searchSizer.Add(labelSearch, 0, wx.ALL, 5)
		searchSizer.Add(self.comboboxOptions, 0, wx.ALL, 5)
		searchSizer.Add(self.search, 0, wx.ALL, 5)
		searchSizer.Add(self.buttonSearch, 0, wx.ALL, 5)

		buttonSizer.Add(self.buttonEdit, 0, wx.ALL | wx.EXPAND, 5)
		buttonSizer.Add(self.buttonDelete, 0, wx.ALL | wx.EXPAND, 5)
		buttonSizer.Add(self.buttonRefresh, 0, wx.ALL | wx.EXPAND, 5)
		buttonSizer.Add(self.buttonImport, 0, wx.ALL | wx.EXPAND, 5)
		buttonSizer.Add(self.buttonExport, 0, wx.ALL | wx.EXPAND, 5)
		buttonSizer.Add(self.buttonResetRecords, 0, wx.ALL | wx.EXPAND, 5)
		buttonSizer.Add(self.buttonExit, 0, wx.ALL | wx.EXPAND, 5)

		boxSizer.Add(searchSizer)
		boxSizer.Add(viewSizer)
		boxSizer.Add(buttonSizer, 0, wx.CENTER)
		panel.SetSizer(boxSizer)

		# Binding events to buttons.
		self.buttonSearch.Bind(wx.EVT_BUTTON, self.onSearch, self.buttonSearch)
		self.buttonEdit.Bind(wx.EVT_BUTTON, self.onEdit, self.buttonEdit)
		self.buttonNew.Bind(wx.EVT_BUTTON, self.onNew, self.buttonNew)
		self.buttonDelete.Bind(wx.EVT_BUTTON, self.onDelete, self.buttonDelete)
		self.buttonRefresh .Bind(
			wx.EVT_BUTTON, self.onToUpdate, self.buttonRefresh)
		self.buttonImport.Bind(
			wx.EVT_BUTTON, self.onToImport, self.buttonImport)
		self.buttonExport.Bind(
			wx.EVT_BUTTON, self.onToExport, self.buttonExport)
		self.buttonResetRecords.Bind(
			wx.EVT_BUTTON, self.onReset, self.buttonResetRecords)
		self.buttonExit.Bind(wx.EVT_BUTTON, self.onClose, self.buttonExit)

		# Creating the columns of the ObjectListView.
	def set_contacts(self):
		self.contactList.SetColumns([
			ColumnDefn(_('Name'), 'left', 200, 'name'),
			ColumnDefn(_('Cell phone'), 'left', 200, 'cell'),
			ColumnDefn(_('Landline'), 'left', 200, 'landline'),
			ColumnDefn(_('Email'), 'left', 200, 'email')
		])
		self.contactList.SetObjects(self.contactResults)

		# Show all records.
	def show_all_records(self):
		self.contactResults = core.get_all_records()
		self.set_contacts()
		self.contactList.SetFocus()

		# Add a new record to the agenda.
	def onNew(self, event):
		dlg = AddEditRecDialog(gui.mainFrame)
		dlg.ShowModal()
		dlg.Destroy()
		self.show_all_records()
		self.contactList.SetFocus()

		# Edit a selected record.
	def onEdit(self, event):
		selectedRow = self.contactList.GetSelectedObject()
		if selectedRow == None:
			# Translators: Dialog when there is no row selected in the
			# ObjectListView.
			wx.MessageBox(_('No row selected!'), _('Error'))
			return
		dlg = AddEditRecDialog(gui.mainFrame, selectedRow,
							   title=_('To edit'), addRecord=False)
		dlg.ShowModal()
		dlg.Destroy()
		self.show_all_records()
		self.contactList.SetFocus()

		# Delete a selected record.
	def onDelete(self, event):
		selectedRow = self.contactList.GetSelectedObject()
		if selectedRow == None:
			# Translators: Dialog when there is no row selected in the
			# ObjectListView.
			wx.MessageBox(_('No row selected!'), _('Error'))
			return
		dlg = wx.MessageDialog(None, _('Do you want to delete the selected record?'), _('Attention'),
							   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		resposta = dlg.ShowModal()
		if resposta == wx.ID_YES:
			core.delete(selectedRow.id)
			wx.MessageBox(_('record deleted!'), _('Success'))
			self.show_all_records()
		self.contactList.SetFocus()

		# Search using all the fields of the agenda.
	def onSearch(self, event):
		filterChoice = self.comboboxOptions.GetValue()
		keyword = self.search.GetValue()
		print(('%s %s' % (filterChoice, keyword)))
		self.contactResults = core.search_records(filterChoice, keyword)
		self.set_contacts()
		self.contactList.SetFocus()

		# Show all records in the ObjectListview's view control.
	def onToUpdate(self, event):
		self.show_all_records()

	# Import csv file to the agenda.
	def onToImport(self, event):
		dlg = wx.FileDialog(self, _('import csv file'),
							os.getcwd(), '', '*.csv', wx.FC_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			try:
				mypath = dlg.GetPath()
				core.to_records(mypath)
			except:
				wx.MessageBox(
					_('It was not possible to import the file!'), _('Attention'))
		dlg.Destroy()
		self.show_all_records()
		self.contactList.SetFocus()

	# Export the calendar to csv.
	def onToExport(self, event):
		dlg = wx.FileDialog(self, _('export csv file'),
							os.getcwd(), 'agenda', '*.csv', wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			try:
				mypath = dlg.GetPath()
				core.to_csv(mypath)
			except:
				wx.MessageBox(
					_('It was not possible to export the file!'), _('Attention'))
		dlg.Destroy()
		self.show_all_records()
		self.contactList.SetFocus()

		# Clear all the agenda.
	def onReset(self, event):
		selectedRow = core.count_records()
		if selectedRow == 0:
			# Translators: Dialog when there is no row selected in the
			# ObjectListView.
			wx.MessageBox(_('The agenda is empty!'), _('Attention'))
			return
		dlg = wx.MessageDialog(None, _('This operation erases all records from the phone book., do you wish to continue?'), _('Attention'),
							   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		resposta = dlg.ShowModal()
		if resposta == wx.ID_YES:
			core.reset_record()
			wx.MessageBox(_('agenda deleted!'), _('Success'))
		self.show_all_records()
		self.contactList.SetFocus()

	# Check and apply settings.
	def set_config(self):
		if config.conf["contactBook"]["resetRecords"] == False:
			self.buttonResetRecords.Disable()
		if (config.conf["contactBook"]["importCSV"] == False) or (config.conf["contactBook"]["exportCSV"] == False):
			self.buttonExport.Disable()
			self.buttonImport.Disable()

		# closes the window.
	def onClose(self, event):
		self.Destroy()
