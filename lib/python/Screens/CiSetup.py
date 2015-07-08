from Screen import Screen
from Screens.HelpMenu import HelpableScreen
from Screens.MessageBox import MessageBox
from Components.InputDevice import iInputDevices
from Components.Sources.StaticText import StaticText
from Components.Sources.Boolean import Boolean
from Components.Sources.List import List
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import config, ConfigSlider, ConfigSubsection, ConfigYesNo, ConfigText, getConfigListEntry, ConfigNothing, ConfigOnOff
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import NumberActionMap, NumberActionMap, HelpableActionMap 
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN
from Tools.LoadPixmap import LoadPixmap
from Tools import Notifications
from enigma import quitMainloop
from Screens.Standby import QuitMainloopScreen
from os import path as os_path
import os

config.ci_setting = ConfigYesNo(default = True)

class CiSetting(Screen, ConfigListScreen):
	skin = """
		<screen name="CiSetting" title="Ci Setup" position="fill" flags="wfNoBorder">
		    <panel name="PigTemplate"/>
		    <widget name="config" position="530,110" size="690,500" scrollbarMode="showOnDemand" selectionPixmap="PLi-HD/buttons/sel.png" />
			<widget source="description" render="Label" position="530,365" size="690,200" transparent="1" font="Regular;21" valign="center" halign="center" />
			<widget source="Statustext" render="Label" position="495,587" size="200,26" transparent="1" zPosition="10" font="Regular;20" valign="center" halign="right" />
		    <ePixmap pixmap="skin_default/buttons/button_red.png" position="305,648" size="220,28" alphatest="on" />
		    <ePixmap pixmap="skin_default/buttons/button_green.png" position="450,648" size="220,28" alphatest="on" />
    		<widget source="key_yellow" render="Label" position="615,643" size="220,28" backgroundColor="darkgrey" zPosition="2" transparent="1" foregroundColor="grey" font="Regular;24" halign="left" />
   			<widget source="key_red" render="Label" position="325,643" size="220,28" backgroundColor="darkgrey" zPosition="2" transparent="1" foregroundColor="grey" font="Regular;24" halign="left" />
    		<widget source="key_green" render="Label" position="470,643" size="220,28" backgroundColor="darkgrey" zPosition="2" transparent="1" foregroundColor="grey" font="Regular;24" halign="left" />
			<widget name="config" position="530,110" size="690,500" scrollbarMode="showOnDemand" selectionPixmap="PLi-HD/buttons/sel.png" />
			<widget source="description" render="Label" position="530,365" size="690,200" transparent="1" font="Regular;21" valign="center" halign="center" />
			<widget source="Statustext" render="Label" position="495,587" size="200,26" transparent="1" zPosition="10" font="Regular;20" valign="center" halign="right" />
	  </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.cisetting_title = _("Activate CI Path")
		self["status"] = StaticText()
		self.enableConfigEntry = None
		self.enableEntry = None
		self.connectEntry = None

		self.list = [ ]
		self.onChangedEntry = [ ]
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)		
		config.lists = ConfigSubsection()
 
		self["description"] = StaticText()
		self["Statustext"] = StaticText()

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("Save"))

		self["actions"] = NumberActionMap(["SetupActions", "MenuActions"],
			{
				"cancel": self.keyCancel,
				"save": self.apply,
				"ok": self.openSelected,
			}, -2)

		if not self.SelectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.SelectionChanged)
		config.lists = ConfigSubsection()
		self.createSetup()
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.cisetting_title)
	
	def SelectionChanged(self):
		self["status"].setText(self["config"].getCurrent())

	def createSetup(self):
		self.list = [ ]
		self.list.append(getConfigListEntry(_("Activate CI Path"), config.ci_setting))

		self["list"] = List(self.list)
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		self.SelectionChanged()
			
	def confirm(self, confirmed):
		if not confirmed:
			print "not confirmed"
			return
		else:
			self.close()

	def apply(self):
		if not config.ci_setting.value:
			os.system("echo no > /proc/stb/cip/cipath_ctrl")
			if os_path.exists("/etc/.ci"):
				os.system("rm /etc/.ci")
			config.ci_setting.save()
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("It will restart your receiver to adapt new option."), MessageBox.TYPE_YESNO, timeout = 20, default = True)
		else:
			os.system("echo yes > /proc/stb/cip/cipath_ctrl")
			if not os_path.exists("/etc/.ci"):
				os.system("touch /etc/.ci")
			config.ci_setting.save()
			self.session.openWithCallback(self.cancelConfirm, MessageBox, _("It will restart your receiver to adapt new option."), MessageBox.TYPE_YESNO, timeout = 20, default = True)

	def cancelConfirm(self, result):
		if result:
			self.quit(2)

	def quit(self, mode):
		if mode == 2:
			self.hide()
			self.quitScreen = self.session.instantiateDialog(QuitMainloopScreen,retvalue=mode)
			self.quitScreen.show()
			quitMainloop(mode)
	def keycancelConfirm(self, result):
		if not result:
			return
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def keyCancel(self):
		if self["config"].isChanged():
			self.session.openWithCallback(self.keycancelConfirm, MessageBox, _("Really close without saving settings?"), MessageBox.TYPE_YESNO, default = True)
		else:
			self.close()
	
	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

	def newConfig(self):
		current = self["config"].getCurrent()
		if current:
			if current == self.enableEntry:
				self.createSetup()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.createSetup()
	
	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.createSetup()
	
	def openSelected(self):
		index = self["list"].getIndex()	

	def buildListEntry(self, Description, image):
		return((icon, description))

	def getCurrentValue(self):
		return str(self["config"].getCurrent()[1].value)

def SetCi():
	import os
	if os_path.exists("/etc/enigma2/settings"):
		for line in open("/etc/enigma2/settings","r").readlines():
			if "config.ci_setting=true" in line:
				os.system("echo yes > /proc/stb/cip/cipath_ctrl")
	if os_path.exists("/etc/.ci"):
		os.system("echo yes > /proc/stb/cip/cipath_ctrl")
	else:
		os.system("echo no > /proc/stb/cip/cipath_ctrl")
