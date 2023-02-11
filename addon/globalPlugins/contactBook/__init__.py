# -*- coding: UTF-8 -*-

# Simple contact book.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 30/11/2022.

# start of the necessary imports for the module to work correctly.
import globalPluginHandler
from scriptHandler import script
import addonHandler
import wx
import gui
from .configPanel import AgendaSettingsPanel
from .contactList import ContactList

# For translation process
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):	

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.create_menu()

	# Menu creation.
	def create_menu(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(AgendaSettingsPanel)
		self.mainMenu = wx.Menu()
		toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu

		# Translators: Lists all contacts registered in the phonebook.
		contactList = self.mainMenu.Append(-1, _('&Contact list'))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_contactList, contactList)

		# Translators: Open the help page.
		help = self.mainMenu.Append(-1, _('&Help'))
		# gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_onHelp, help)

		# Translators: Menu About the add-on.
		about = self.mainMenu.Append(-1, _('&About'))
		# gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.script_showAbout, about)

		# Translators: Creates the item in the NVDA menu.
		toolsMenu.AppendSubMenu(self.mainMenu, _('&contact book'))

	@script(gesture='kb:Windows+alt+L', description=_('Displays a window with all contacts registered in the phonebook.'), category=_('Contact Book'))
	def script_contactList(self, gesture):
		# Tradutors: Title of contact list dialog box.
		self.dlg = ContactList(gui.mainFrame, _('Contact list.'))
		gui.mainFrame.prePopup()
		self.dlg.Show()
		self.dlg.CentreOnScreen()
		gui.mainFrame.postPopup()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(AgendaSettingsPanel)