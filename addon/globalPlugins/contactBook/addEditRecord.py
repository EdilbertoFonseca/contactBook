# -*- coding: UTF-8 -*-

# Dialog box for adding and editing records.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# start of the necessary imports for the module to work correctly.
import addonHandler
import config
import wx
from .lib.masked import TextCtrl
from .manage import controller as core

# For translation process
addonHandler.initTranslation()


class AddEditRecDialog(wx.Dialog):


	def __init__(self, parent, row=None, title=_('Adicionar'), addRecord=True):
		# Dialog window title.
		self.title = title

		wx.Dialog.__init__(self, parent, title=_('{} Registro').format(title))
		# Check and apply settings.
		if config.conf["contactBook"]["formatPhone"] == False:
			self.formatCell = '(##) #####-####'
			self.formatLandline = '(##) ####-####'
		else:
			self.formatCell = ''
			self.formatLandline = ''

		self.addRecord = addRecord
		self.selectedRow = row
		if row:
			name = self.selectedRow.name
			cell = self.selectedRow.cell
			landline  = self.selectedRow.landline 
			email = self.selectedRow.email
		else:
			name = cell = landline = email = ''

		size = (100, -1)
		font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD) 

		# Creating the widgets.
		self.panel = wx.Panel(self)
		self.labelMSG = wx.StaticText(self.panel, label=_('Novo registro'))
		self.labelMSG.SetFont(font)

		font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
		labelName = wx.StaticText(self.panel, label=_('Nome: '), size=size)
		labelName.SetFont(font)
		self.textName = wx.TextCtrl(self.panel, value=name)

		labelCell = wx.StaticText(self.panel, label=_('Celular: '), size=size)
		labelCell.SetFont(font)
		self.textCell = TextCtrl(self.panel, value=cell, mask=self.formatCell)

		labelLandline  = wx.StaticText(self.panel, label=_('Telefone fixo:'), size=size)
		labelLandline .SetFont(font)
		self.textLandline = TextCtrl(self.panel, value=landline , mask=self.formatLandline)

		labelEmail = wx.StaticText(self.panel, label=_('E-mail: '), size=size)
		labelEmail.SetFont(font)
		self.textEmail = wx.TextCtrl(self.panel, value=email)

		buttonOk = wx.Button(self.panel, wx.ID_OK, label=_('&%s contato') %title)
		buttonCancel = wx.Button(self.panel, wx.ID_CANCEL, label=_('&Fechar'))

		# Binding events to buttons.
		buttonOk.Bind(wx.EVT_BUTTON, self.onRecord)
		buttonCancel.Bind(wx.EVT_BUTTON, self.onClose)

		# Creating the screen objects.
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(self.labelMSG, 0, wx.CENTER)

		viewSizer = wx.BoxSizer(wx.HORIZONTAL)
		viewSizer.Add(self.rowBuilder([labelName, self.textName]), 0, wx.EXPAND)
		viewSizer.Add(labelCell, 0, wx.ALL, 5)
		viewSizer.Add(self.textCell, 1, wx.EXPAND|wx.ALL, 5)
		viewSizer.Add(labelLandline , 0, wx.ALL, 5)
		viewSizer.Add(self.textLandline, 1, wx.EXPAND|wx.ALL, 5)
		viewSizer.Add(self.rowBuilder([labelEmail, self.textEmail]) ,0, wx.EXPAND)

		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer.Add(buttonOk, 0, wx.ALL, 5)
		buttonSizer.Add(buttonCancel, 0, wx.ALL, 5)

		mainSizer.Add(viewSizer, 0, wx.EXPAND)
		mainSizer.Add(buttonSizer, 0, wx.CENTER)
		self.panel.SetSizer(mainSizer)

	def getData(self):
		contactDict = {}

		Name = self.textName.GetValue()
		Cell = self.textCell.GetValue()
		landline  = self.textLandline.GetValue()
		Email = self.textEmail.GetValue()
		if Name == '' or Cell == '' or landline == '':
			# Translators: Dialog displayed when one of the required fields is empty.
			wx.MessageBox(_('Nome, celular e telefone fixo são obrigatórios!'),
									  _('Erro'))
			return
		if '-' in Email:
			Email = Email.replace("-", "")
		contactDict['name'] = Name
		contactDict['cell'] = Cell
		contactDict['landline'] = landline 
		contactDict['email'] = Email
		return contactDict

		# Adding the records to the database.
	def onAdd(self):
		contactDict = self.getData()
		data = ({'contacts':contactDict})
		core.add_record(data)

		# Translators:  Dialog displayed upon completion.
		wx.MessageBox(_('Contato adicionado'),
								  _('Sucesso!'), wx.ICON_INFORMATION)

		# Clear all fields to add a new record.
		for child in self.panel.GetChildren():
			if isinstance(child, wx.TextCtrl):
				child.SetValue("")

	# Cancels the dialog.
	def onClose(self, event):
		self.Destroy()
		
	def onEdit(self):
		contactDict = self.getData()
		core.edit_record(self.selectedRow.id, contactDict)

		# Translators:  Dialog displayed after editing is complete.
		wx.MessageBox(_('Contato editado com sucesso!'), _('Sucesso'),
		wx.ICON_INFORMATION)
		self.Destroy()

	def onRecord(self, event):
		if self.addRecord:
			self.onAdd()
		else:
			self.onEdit()
		self.textName.SetFocus()

	def rowBuilder(self, widgets):
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		lbl, txt = widgets
		sizer.Add(lbl, 0, wx.ALL, 5)
		sizer.Add(txt, 1, wx.EXPAND|wx.ALL, 5)
		return sizer
