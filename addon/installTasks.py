# -*- coding: UTF-8 -*-

# Simple contact book.
# Author: Edilberto Fonseca.
# E-mail: <edilberto.fonseca@outlook.com>
# Creation date: 03/03/2023.

# Standard Python imports
import os

# Imports from NVDA.
import globalVars
import addonHandler

# Define add-on installation tasks.
def onInstall():
	configFilePath = os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", "contactBook", "globalPlugins", "contactBook", "database.db"))
	if os.path.isfile(configFilePath):
				os.rename(configFilePath, os.path.abspath(os.path.join(globalVars.appArgs.configPath, "addons", "contactBook" +
															addonHandler.ADDON_PENDINGINSTALL_SUFFIX, "globalPlugins", "contactBook", "database.db")))
