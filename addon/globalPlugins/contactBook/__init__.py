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
from .contactList import ContactList

# Start the initDB function.
Section.initDB()

# For translation process
addonHandler.initTranslation()

initConfiguration()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

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

		# Translators: Menu About the add-on.
		about = self.mainMenu.Append(-1, _('&About'))
		gui.mainFrame.sysTrayIcon.Bind(
			wx.EVT_MENU, self.script_showAbout, about)

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

	@script(gesture='kb:Windows+alt+O', description=_('About the Contact Book Add-on.'), category=_('Contact Book'))
	def script_showAbout(self, gesture):
		def showAbout():
			summary = _('Summary: {}\n').format(
				addonHandler.getCodeAddon().manifest['summary'])
			version = _('Version: {}\n').format(
				addonHandler.getCodeAddon().manifest['version'])
			description = _('Description: {}\n').format(
				addonHandler.getCodeAddon().manifest['description'])
			author = _('Autor: {}\n\n').format(
				addonHandler.getCodeAddon().manifest['author'])
			minimumNVDAVersion = _('Minimum version of NVDA required: {}\n').format(
				addonHandler.getCodeAddon().manifest['minimumNVDAVersion'])
			lastTestedNVDAVersion = _('Latest version of NVDA tested: {}').format(
				addonHandler.getCodeAddon().manifest['lastTestedNVDAVersion'])

			gui.messageBox(  # Translators: About the addon.
				summary +
				version +
				description +
				author +
				minimumNVDAVersion +
				lastTestedNVDAVersion,
				_('Add-on information'))
		wx.CallAfter(showAbout)

	@script(gesture='kb:Windows+alt+J', description=_('Opens the Contact Book add-on help page.'), category=_('Contact Book'))
	def script_onHelp(self, gesture):
		"""Open the addon's help page"""
		wx.LaunchDefaultBrowser(addonHandler.Addon(os.path.join(
			os.path.dirname(__file__), "..", "..")).getDocFilePath())

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(
			AgendaSettingsPanel)
