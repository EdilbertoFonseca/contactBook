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
			wx.CheckBox(self, label=_("&Não usar formatação de telefone"))
		)
		self.formatPhone.SetValue(config.conf["contactBook"]["formatPhone"])

		self.resetRecords = agendaHelper.addItem(
			# Translators: Checkbox text to display scheduler reset button..
			wx.CheckBox(self, label=_("&Exibir a opção para apagar toda a agenda"))
		)
		self.resetRecords.SetValue(config.conf["contactBook"]["resetRecords"])

		self.importCSV = agendaHelper.addItem(
			# Translators: Checkbox text to display import csv files to database button.
			wx.CheckBox(self, label=_("&Exibir o botão importar arquivo CSV"))
		)
		self.importCSV.SetValue(config.conf["contactBook"]["importCSV"])


		self.exportCSV = agendaHelper.addItem(
			# Translators: Checkbox text to display export csv files to database button.
			wx.CheckBox(self, label=_("&Exibir o botão exportar arquivo CSV"))
		)
		self.exportCSV.SetValue(config.conf["contactBook"]["exportCSV"])

	def postInit(self):
		self.formatPhone.SetFocus()

	# Salva as opções no arquivo de configuração do NVDA.
	def onSave(self):
		config.conf["contactBook"]["formatPhone"] = self.formatPhone.GetValue()
		config.conf["contactBook"]["resetRecords"] = self.resetRecords.GetValue()
		config.conf["contactBook"]["importCSV"] = self.importCSV.GetValue()
		config.conf["contactBook"]["exportCSV"] = self.exportCSV.GetValue()

	def terminate(self):
		super(AgendaSettingsPanel, self).terminate()
		pass


