# -*- coding: UTF-8 -*-

# Calendar configuration panel.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 24/01/2023.

# start of the necessary imports for the module to work correctly.
import addonHandler
import gui
import wx
import config

# For translation process
addonHandler.initTranslation()

# Retrieves the summary text of the manifest.
addonSumary = addonHandler.getCodeAddon().manifest["summary"]

# Setup started by default.
confspec = {
	"formatPhone": "boolean(default=False)",
	"resetRecords": "boolean(default=False)",
	"importCSV": "boolean(default=False)",
	"exportCSV": "boolean(default=False)"
}
config.conf.spec["contactBook"] = confspec


class AgendaSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the Agenda settings dialog in the NVDA settings.
	title = addonSumary

	def makeSettings(self, settingsSizer):
		agendaHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		self.formatPhone = agendaHelper.addItem(
			# Translators: Phone formatting checkbox text.
			wx.CheckBox(self, label=_('&Do not use phone formatting'))
		)
		self.formatPhone.SetValue(config.conf["contactBook"]["formatPhone"])

		self.resetRecords = agendaHelper.addItem(
			# Translators: Checkbox text to display scheduler reset button..
			wx.CheckBox(self, label=_('&Show option to delete entire calendar'))
		)
		self.resetRecords.SetValue(config.conf["contactBook"]["resetRecords"])

		self.importCSV = agendaHelper.addItem(
			# Translators: Checkbox text to display import csv files to database button.
			wx.CheckBox(self, label=_('&Show import CSV file button'))
		)
		self.importCSV.SetValue(config.conf["contactBook"]["importCSV"])


		self.exportCSV = agendaHelper.addItem(
			# Translators: Checkbox text to display export csv files to database button.
			wx.CheckBox(self, label=_('&Show export CSV file button'))
		)
		self.exportCSV.SetValue(config.conf["contactBook"]["exportCSV"])

	def postInit(self):
		self.formatPhone.SetFocus()

	#Saves options to NVDA's configuration file.
	def onSave(self):
		config.conf["contactBook"]["formatPhone"] = self.formatPhone.GetValue()
		config.conf["contactBook"]["resetRecords"] = self.resetRecords.GetValue()
		config.conf["contactBook"]["importCSV"] = self.importCSV.GetValue()
		config.conf["contactBook"]["exportCSV"] = self.exportCSV.GetValue()

	def terminate(self):
		super(AgendaSettingsPanel, self).terminate()
		pass


