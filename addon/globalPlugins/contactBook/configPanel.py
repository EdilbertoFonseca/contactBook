# -*- coding: UTF-8 -*-

# Calendar configuration panel.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 24/01/2023.

# For update process
from .update import *

# Standard Python imports.
import os

# Standard NVDA imports.
import addonHandler
import gui
import config
from configobj import ConfigObj
import wx

# For translation process
addonHandler.initTranslation()

# Retrieves the summary text of the manifest.
addonSumary = addonHandler.getCodeAddon().manifest["summary"]

# Read configuration on INI file to know where are the agenda.db files...
dirDatabase = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons",
										   "contactBook", "globalPlugins", "contactBook", "manage", "agenda.db"))
firstDatabase = ""
altDatabase = ""
indexDB = 0

try:
	if config.conf[ourAddon.name]["xx"]:
		# index of agenda.db file to use
		indexDB = int(config.conf[ourAddon.name]["xx"])
		if indexDB == 0:
			dirDatabase = config.conf[ourAddon.name]["path"]
		else:
			dirDatabase = config.conf[ourAddon.name]["altPath"]
		firstDatabase = config.conf[ourAddon.name]["path"]
		altDatabase = config.conf[ourAddon.name]["altPath"]
except:
	# Not registered, so use the default path
	pass


class AgendaSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the Agenda settings dialog in the NVDA settings.
	title = addonSumary

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(
			self, sizer=settingsSizer)

		# Translators: Phone formatting checkbox text.
		self.formatPhone = wx.CheckBox(
			self, label=_('&Do not use phone formatting'))
		self.formatPhone.SetValue(config.conf[ourAddon.name]["formatPhone"])
		settingsSizerHelper.addItem(self.formatPhone)

		# Translators: Checkbox text to display scheduler reset button..
		self.resetRecords = wx.CheckBox(self, label=_(
			'&Show option to delete entire calendar'))
		self.resetRecords.SetValue(config.conf[ourAddon.name]["resetRecords"])
		settingsSizerHelper.addItem(self.resetRecords)

		# Translators: Checkbox text to display import csv files to database
		# button.
		self.importCSV = wx.CheckBox(
			self, label=_('&Show import CSV file button'))
		self.importCSV.SetValue(config.conf[ourAddon.name]["importCSV"])
		settingsSizerHelper.addItem(self.importCSV)

		# Translators: Checkbox text to display export csv files to database
		# button.
		self.exportCSV = wx.CheckBox(
			self, label=_('&Show export CSV file button'))
		self.exportCSV.SetValue(config.conf[ourAddon.name]["exportCSV"])
		settingsSizerHelper.addItem(self.exportCSV)

		# Translators: Name of combobox with the agenda files path
		pathBoxSizer = wx.StaticBoxSizer(
			wx.HORIZONTAL, self, label=_("Path of agenda files:"))
		pathBox = pathBoxSizer.GetStaticBox()
		pathGroup = guiHelper.BoxSizerHelper(self, sizer=pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)

		global firstDatabase
		if firstDatabase == "":
			firstDatabase = dirDatabase
		self.pathList = [firstDatabase, altDatabase]
		self.pathNameCB = pathGroup.addLabeledControl(
			"", wx.Choice, choices=self.pathList)
		self.pathNameCB.SetSelection(indexDB)

		# Translators: This is the label for the button used to add or change a
		# agenda.db location
		changePathBtn = wx.Button(
			pathBox, label=_("&Select or add a directory"))
		changePathBtn.Bind(wx.EVT_BUTTON, self.OnDirectory)

	def OnDirectory(self, event):
		self.Freeze()
		global dirDatabase, firstDatabase, altDatabase, indexDB
		lastDir = os.path.dirname(__file__)
		dDir = lastDir
		dFile = "agenda.db"
		frame = wx.Frame(None, -1, 'teste')
		frame.SetSize(0, 0, 200, 50)
		dlg = wx.FileDialog(frame, _("Choose where to save the agenda file"), dDir, dFile,
							wildcard=_("Database files (*.db)"),
							style=wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			fname = dlg.GetPath()
			index = self.pathNameCB.GetSelection()
			if index == 0:
				if os.path.exists(fname):
					firstDatabase = fname
				else:
					os.rename(firstDatabase, fname)
					firstDatabase = fname
			else:
				if os.path.exists(fname):
					altDatabase = fname
				else:
					if altDatabase == "":
						altDatabase = fname
					else:
						os.rename(altDatabase, fname)
						altDatabase = fname
			dirDatabase = fname
			self.pathList = [firstDatabase, altDatabase]
		dlg.Close()
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()
		event.Skip()

	# Saves options to NVDA's configuration file.
	def onSave(self):
		global dirDatabase, indexDB
		config.conf[ourAddon.name]["formatPhone"] = self.formatPhone.GetValue()
		config.conf[ourAddon.name]["resetRecords"] = self.resetRecords.GetValue()
		config.conf[ourAddon.name]["importCSV"] = self.importCSV.GetValue()
		config.conf[ourAddon.name]["exportCSV"] = self.exportCSV.GetValue()
		config.conf[ourAddon.name]["path"] = firstDatabase
		config.conf[ourAddon.name]["altPath"] = altDatabase
		config.conf[ourAddon.name]["xx"] = str(
			self.pathList.index(self.pathNameCB.GetStringSelection()))
		config.conf.save()
		indexDB = self.pathNameCB.GetSelection()
		dirDatabase = self.pathList[indexDB]

	def terminate(self):
		super(AgendaSettingsPanel, self).terminate()
		pass
