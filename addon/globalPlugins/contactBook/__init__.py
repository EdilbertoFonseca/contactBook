# -*- coding: UTF-8 -*-

# Simple contact book.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# Standard Python imports.
import os

# Standard NVDA imports.
import globalPluginHandler
from scriptHandler import script
import addonHandler
import wx
import gui

# imports from the Contact Book addon.
from .manage.model import Section
from .configPanel import *
from .main import ContactList

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Start the initDB function.
Section.initDB()

# For translation process
addonHandler.initTranslation()

initConfiguration()

def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.create_menu()

	# Menu creation.
	def create_menu(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(
			AgendaSettingsPanel)
		self.mainMenu = wx.Menu()
		toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Lists all contacts registered in the phonebook.
		contactList = self.mainMenu.Append(-1, _('&Contact list'))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_contactList, contactList)

		# Translators: Open the help page.
		help = self.mainMenu.Append(-1, _('&Help'))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_onHelp, help)

		# Translators: Creates the item in the NVDA menu.
		toolsMenu.AppendSubMenu(self.mainMenu, _('&contact book'))

	#defining a script with decorator:
	@script(
		gesture='kb:Windows+alt+L',

		# Translators: Text displayed in NVDA help.
		description=_('Displays a window with all contacts registered in the phonebook.'),
		category=ADDON_SUMMARY
		)
	def script_contactList(self, gesture):
		# Translators: Title of contact list dialog box.
		self.dlg = ContactList(gui.mainFrame, _('Contact list.'))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.CentreOnScreen()
		gui.mainFrame.postPopup()

	#defining a script with decorator:
	@script(
		gesture='kb:Windows+alt+J',

		# Translators: Text displayed in NVDA help.
		description=_('Opens the Contact Book add-on help page.'),
		category=ADDON_SUMMARY
)
	def script_onHelp(self, gesture):
		"""Open the addon's help page"""
		wx.LaunchDefaultBrowser(addonHandler.Addon(os.path.join(
			os.path.dirname(__file__), "..", "..")).getDocFilePath())

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
			AgendaSettingsPanel)
		try:
			self.toolsMenu.Remove(self.mainMenu)
		except Exception:
			pass
