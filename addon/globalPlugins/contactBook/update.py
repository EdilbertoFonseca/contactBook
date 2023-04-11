# -*- coding: UTF-8 -*-

# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 03/03/2023.

# Update add-ons module based on the work of several add-on authors
# This file is covered by the GNU General Public License.
#
# You just need to place this module in the appModule or globalPlugin
# folder and include in the __init__.py file in the import section:
"""
# For update process
from .update import *
"""
# and in the def __init__(self):
"""
		_MainWindows = Initialize()
		_MainWindows.start()
"""

# Standard Python imports.
import os

# Standard NVDA imports.
import globalVars
import addonHandler
import addonHandler.addonVersionCheck
import config
import gui
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper

# For translation
addonHandler.initTranslation()


def getOurAddon():
	return addonHandler.getCodeAddon()


ourAddon = getOurAddon()
bundle = getOurAddon()


def initConfiguration():
# Define the plugin specifications
	confspec = {
		"formatPhone": "boolean(default=False)",
		"resetRecords": "boolean(default=False)",
		"importCSV": "boolean(default=False)",
		"exportCSV": "boolean(default=False)",
		"path": "string(default="")",
		"altPath ": "string(default="")",
		"xx": "string(default="")",
	}

# Update NVDA configuration file specs
	config.conf.spec[ourAddon.name] = confspec


initConfiguration()
