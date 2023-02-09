# -*- coding: UTF-8 -*-

# Lists all contacts registered in the phonebook.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# start of the necessary imports for the module to work correctly.
import addonHandler
import gui
import ui
import config
import os
import wx
from .lib import csv
from .lib.ObjectListView import ObjectListView, ColumnDefn
from .addEditRecord import AddEditRecDialog
from .manage import controller as core

# For translation process
addonHandler.initTranslation()

class ContactList(wx.Dialog):


	def __init__(self, parent, title):
		# Title of contact list dialog.
		self.title = title
		try:
			self.contactResults =  core.get_all_records()
		except:
			self.contactResults = []

		super(ContactList, self).__init__(parent, title=title)
		listOfOptions = ['Nome', 'Celular', 'Telefone fixo', 'E-mail'] # List of combobox choices option.

		# Creating the screen objects.
		panel = wx.Panel(self)
		labelSearch = wx.StaticText(panel, label=_('Procurar por: '))
		self.comboboxOptions = wx.ComboBox(panel, value='Nome', choices=listOfOptions)
		self.search = wx.SearchCtrl(panel, -1)
		self.buttonSearch = wx.Button(panel, label=_('&Buscar'))
		self.contactList = ObjectListView(panel, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.contactList.SetEmptyListMsg(_('Nenhum registro foi encontrado!'))
		self.set_contacts()

		self.buttonEdit = wx.Button(panel, wx.ID_EDIT, label=_('&Editar'))
		self.buttonNew= wx.Button(panel, wx.ID_NEW, label=_('&Novo'))
		self.buttonDelete = wx.Button(panel, wx.ID_DELETE, label=_('&Remover'))
		self.buttonUpdate = wx.Button(panel, -1, label=_('&Atualizar'))
		self.buttonImport = wx.Button(panel, wx.ID_DELETE, label=_('&Importar csv...'))
		self.buttonExport = wx.Button(panel, wx.ID_DELETE, label=_('E&xportar csv...'))
		self.buttonResetRecords = wx.Button(panel, -1, label=_('Apagar todos os regis&tros.'))
		self.buttonExit = wx.Button(panel, wx.ID_CANCEL, label=_('&Sair'))
		self.set_config()

		# Creating the layout and adding it to the panel.
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		searchSizer = wx.BoxSizer(wx.HORIZONTAL)
		viewSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		searchSizer.Add(labelSearch, 0, wx.ALL, 5)
		searchSizer.Add(self.comboboxOptions, 0, wx.ALL, 5)
		searchSizer.Add(self.search, 0, wx.ALL, 5)
		searchSizer.Add(self.buttonSearch, 0, wx.ALL, 5)
		viewSizer.Add(self.contactList, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonEdit, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonDelete, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonUpdate, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonImport, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonExport, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonResetRecords, 0, wx.ALL|wx.EXPAND, 5)
		buttonSizer.Add(self.buttonExit, 0, wx.ALL|wx.EXPAND, 5)
		boxSizer.Add(searchSizer)
		boxSizer.Add(viewSizer)
		boxSizer.Add(buttonSizer, 0, wx.CENTER)
		panel.SetSizer(boxSizer)

		# Binding events to buttons.
		self.buttonSearch.Bind(wx.EVT_BUTTON, self.onSearch, self.buttonSearch)
		self.buttonEdit.Bind(wx.EVT_BUTTON, self.onEdit, self.buttonEdit)
		self.buttonNew.Bind(wx.EVT_BUTTON, self.onNew, self.buttonNew)
		self.buttonDelete.Bind(wx.EVT_BUTTON, self.onDelete, self.buttonDelete)
		self.buttonUpdate.Bind(wx.EVT_BUTTON, self.onToUpdate, self.buttonUpdate)
		self.buttonImport.Bind(wx.EVT_BUTTON, self.onToImport, self.buttonImport)
		self.buttonExport.Bind(wx.EVT_BUTTON, self.onToExport, self.buttonExport)
		self.buttonResetRecords.Bind(wx.EVT_BUTTON, self.onReset, self.buttonResetRecords)
		self.buttonExit.Bind(wx.EVT_BUTTON, self.onClose, self.buttonExit)

		# Creating the columns of the ObjectListView.
	def set_contacts(self):
		self.contactList.SetColumns([
			ColumnDefn(_('Nome'), 'left', 200, 'name'),
			ColumnDefn(_('CELULAR'), 'left', 200, 'cell'),
			ColumnDefn(_('Telefone fixo'), 'left', 200, 'landline'),
			ColumnDefn(_('E-mail'), 'left', 200, 'email')
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

		# Edit a selected record.
	def onEdit(self, event):
		selectedRow = self.contactList.GetSelectedObject()
		if selectedRow == None:
			# Translators: Dialog when there is no row selected in the ObjectListView.
			wx.MessageBox(_('Nenhuma linha selecionada!'), _('Erro'))
			return
		dlg = AddEditRecDialog( gui.mainFrame, selectedRow, title=_('Editar'), addRecord=False)
		dlg.ShowModal()
		dlg.Destroy()
		self.show_all_records()

		# Delete a selected record.
	def onDelete(self, event):
		selectedRow = self.contactList.GetSelectedObject()
		if selectedRow == None:
			# Translators: Dialog when there is no row selected in the ObjectListView.
			wx.MessageBox(_('Nenhuma linha selecionada!'), _('Erro'))
			return
		dlg = wx.MessageDialog(None, _('Deseja apagar o registro selecionado!'), _('Atenção'),
		wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		resposta = dlg.ShowModal()
		if resposta == wx.ID_YES:
			core.delete(selectedRow.id)		
			wx.MessageBox(_('Registro apagado !'), _('Sucesso'))
			self.show_all_records()

		# Search using all the fields of the agenda.
	def onSearch(self, event):
		filterChoice = self.comboboxOptions.GetValue()
		keyword = self.search.GetValue()
		print(('%s %s' %(filterChoice, keyword)))
		self.contactResults = core.search_records(filterChoice, keyword)
		self.set_contacts()

		# Show all records in the ObjectListview's view control.
	def onToUpdate(self, event):
		self.show_all_records()
	# Import csv file to the agenda.
	def onToImport(self, event):
		dlg = wx.FileDialog(self, 'Importar arquivo csv', os.getcwd(), '', '*.csv', wx.FC_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			try:
				mypath = dlg.GetPath()
				core.to_records(mypath)
			except:
				wx.MessageBox('Não foi pocivel inportar o arquivo!', 'Atenção')
		dlg.Destroy()
		self.show_all_records()

	# Exporta da agenda para csv.
	def onToExport(self, event):
		dlg = wx.FileDialog(self, 'Exportar arquivo csv', os.getcwd(), 'agenda', '*.csv', wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			try:
				mypath = dlg.GetPath()
				core.to_csv(mypath)
			except:
				wx.MessageBox('Não foi pocivel exportar o arquivo!', 'Atenção')
		dlg.Destroy()
		self.show_all_records()

		# Clear all the agenda.
	def onReset(self, event):
		selectedRow = core.count_records()
		if selectedRow == 0:
			# Translators: Dialog when there is no row selected in the ObjectListView.
			wx.MessageBox('A agenda está vasia!', 'Atenção')
			return
		dlg = wx.MessageDialog(None, 'Essa operação  apaga todos os registros da agenda, deseja continuar!', 'Atenção',
		wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		resposta = dlg.ShowModal()
		if resposta == wx.ID_YES:
			core.reset_record()
			wx.MessageBox('Agenda apagada!', 'Sucesso')
		self.show_all_records()

	# Check and apply settings.
	def set_config(self):
		if config.conf["contactBook"]["resetRecords"] == False:
			self.buttonResetRecords.Disable()
		if(config.conf["contactBook"]["importCSV"] == False) or (config.conf["contactBook"]["exportCSV"] == False):
			self.buttonExport.Disable()
			self.buttonImport.Disable()

		# closes the window.
	def onClose(self, event):
		self.Destroy()