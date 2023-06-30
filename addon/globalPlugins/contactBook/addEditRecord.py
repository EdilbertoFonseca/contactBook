# -*- coding: UTF-8 -*-

# Dialog box for adding and editing records.
# Author: Edilberto Fonseca.
# Email: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# Standard NVDA imports.
import addonHandler
import config
import os
import wx
import gui

# Non-standard Python imports from NVDA.
import sys
baseDir = os.path.dirname(__file__)
libs = os.path.join(baseDir, "lib")
sys.path.append(libs)
from  masked import TextCtrl

# imports from the Contact Book addon.
from . import controller as core
from .update import *

# For translation process
addonHandler.initTranslation()


class AddEditRecDialog(wx.Dialog):

	def __init__(self, parent, row=None, title=_('Add'), addRecord=True):
		# Dialog window title.
		self.title = title
		WIDTH = 600
		HEIGHT = 300

		wx.Dialog.__init__(self, parent, title=_('{} Record').format(title), size=(WIDTH, HEIGHT))
		# Check and apply settings.
		self.formatCellPhone = config.conf[ourAddon.name]["formatCellPhone"]
		self.formatLandline = config.conf[ourAddon.name]["formatLandline"]

		self.addRecord = addRecord
		self.selectedRow = row
		if row:
			name = self.selectedRow.name
			cell = self.selectedRow.cell
			landline = self.selectedRow.landline
			email = self.selectedRow.email
		else:
			name = cell = landline = email = ''

		# Creating the widgets.
		self.panel = wx.Panel(self)
		labelName = wx.StaticText(self.panel, label=_('Name: '))
		self.textName = wx.TextCtrl(self.panel, -1, value=name, size=(200, 25))

		labelCell = wx.StaticText(self.panel, label=_('Cell phone: '))
		self.textCell = TextCtrl(self.panel, value=cell, mask=self.formatCellPhone)

		labelLandline = wx.StaticText(self.panel, label=_('Landline: '))
		self.textLandline = TextCtrl(
			self.panel, value=landline, mask=self.formatLandline)

		labelEmail = wx.StaticText(self.panel, label=_('Email: '))
		self.textEmail = wx.TextCtrl(self.panel, value=email, size=(200, 25))

		buttonOk = wx.Button(self.panel, wx.ID_OK, label=_('&Ok'))
		buttonCancel = wx.Button(self.panel, wx.ID_CANCEL, label=_('&Cancel'))

		# Binding events to buttons.
		buttonOk.Bind(wx.EVT_BUTTON, self.onRecord)
		buttonCancel.Bind(wx.EVT_BUTTON, self.onClose)

		# Creating the screen objects.
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		viewSizer = wx.BoxSizer(wx.VERTICAL)
		viewSizer.Add(labelName, 0, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(self.textName, 1, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(labelCell, 0, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(self.textCell, 0, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(labelLandline, 0, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(self.textLandline, 0, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(labelEmail, 0, wx.ALL | wx.EXPAND, 5)
		viewSizer.Add(self.textEmail, 0, wx.ALL | wx.EXPAND, 5)

		buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
		buttonSizer.Add(buttonOk, 0, wx.ALL, 5)
		buttonSizer.Add(buttonCancel, 0, wx.ALL, 5)

		mainSizer.Add(viewSizer, wx.EXPAND)
		mainSizer.Add(buttonSizer, 0, wx.CENTER)
		self.panel.SetSizerAndFit(mainSizer)

	def getData(self):
		contactDict = {}

		Name = self.textName.GetValue()
		Cell = self.textCell.GetValue()
		landline = self.textLandline.GetValue()
		Email = self.textEmail.GetValue()
		if Name == '' or Cell == '' or landline == '':
			# Translators: Dialog displayed when one of the required fields is
			# empty.
			gui.messageBox(_('Name, mobile and landline are required!'),
						  _('Error'))
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
		data = ({'contacts': contactDict})
		core.add_record(data)

		# Translators:  Dialog displayed upon completion.
		gui.messageBox(_('Added contact'),
					  _('Success!'), wx.ICON_INFORMATION)

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
		wx.MessageBox(_('Contact edited!'), _('Success'),
					  wx.ICON_INFORMATION)
		self.Destroy()

	def onRecord(self, event):
		if self.addRecord:
			self.onAdd()
		else:
			self.onEdit()
		self.textName.SetFocus()
