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
import os
from enigma import SR

class Mode4DSSetup(Screen, ConfigListScreen):
	skin = """
		<screen name="Mode4DSSetup" title="4DS mode Setup" position="fill" flags="wfNoBorder">
			<ePixmap pixmap="skin_default/buttons/button_red.png" position="305,648" size="220,28" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/button_green.png" position="450,648" size="220,28" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/button_yellow.png" position="595,648" size="220,28" alphatest="on" />
			<widget source="key_yellow" render="Label" position="615,643" size="220,28" backgroundColor="darkgrey" zPosition="2" transparent="1" foregroundColor="grey" font="Regular;24" halign="left" />
			<widget source="key_red" render="Label" position="325,643" size="220,28" backgroundColor="darkgrey" zPosition="2" transparent="1" foregroundColor="grey" font="Regular;24" halign="left" />
			<widget source="key_green" render="Label" position="470,643" size="220,28" backgroundColor="darkgrey" zPosition="2" transparent="1" foregroundColor="grey" font="Regular;24" halign="left" />
			<widget name="config" position="530,110" size="690,500" scrollbarMode="showOnDemand" selectionPixmap="PLi-HD/buttons/sel.png" />
			<widget source="description" render="Label" position="530,365" size="690,200" transparent="1" font="Regular;21" valign="center" halign="center" />
			<widget source="Statustext" render="Label" position="495,587" size="200,26" transparent="1" zPosition="10" font="Regular;20" valign="center" halign="right" />
			<widget name="statuspic" position="1200,135" size="35,25" transparent="1" zPosition="10" pixmaps="skin_default/icons/lock_on.png,skin_default/icons/lock_off.png" alphatest="on" />
	  </screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.mode4ds_title = _("LAN Setting")
		self["status"] = StaticText()
		self.enableConfigEntry = None
		self.enableEntry = None
		self.connectEntry = None
		self.list = [ ]
		self.onChangedEntry = [ ]
		self.mode_4dssetup = ConfigOnOff(default = os.path.exists("/etc/.4dsmode"))
		ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)		
		config.lists = ConfigSubsection()
 
		self["description"] = StaticText()
		self["Statustext"] = StaticText()
		self["statuspic"] = MultiPixmap()
		self["statuspic"].hide()

		if os.path.exists("/etc/.4dsmode"):
			self["key_red"] = StaticText(_("Cancel"))
			self["key_green"] = StaticText(_("Save"))
			self["key_yellow"] = StaticText(_("Download Key"))

			self["actions"] = NumberActionMap(["SetupActions", "MenuActions", "ColorActions" ],
				{
					"cancel": self.keyCancel,
					"save": self.apply,
					"menu": self.closeRecursive,
					"ok": self.openSelected,
					"yellow": self.downloadKey,
				}, -2)
		else:
			self["key_red"] = StaticText(_("Cancel"))
			self["key_green"] = StaticText(_("Save"))

			self["actions"] = NumberActionMap(["SetupActions", "MenuActions"],
				{
					"cancel": self.keyCancel,
					"save": self.apply,
					"menu": self.closeRecursive,
					"ok": self.openSelected,
				}, -2)

		if not self.SelectionChanged in self["config"].onSelectionChanged:
			self["config"].onSelectionChanged.append(self.SelectionChanged)
		config.lists = ConfigSubsection()
		self.createSetup()
		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.mode4ds_title)
	
	def SelectionChanged(self):
		self["status"].setText(self["config"].getCurrent())

	def createSetup(self):
		self.list = [ ]
		string = _("LAN Setting On/Off")

		self.enableEntry = getConfigListEntry(string, self.mode_4dssetup)

		if self.enableEntry:
			if isinstance(self.enableEntry[1], ConfigOnOff):
				self.enableConfigEntry = self.enableEntry[1]

		self.list.append(self.enableEntry)

		self["statuspic"].hide()
		if self.enableConfigEntry:
			if os.path.exists("/etc/.4dsmode"):
				self.list.append(getConfigListEntry(_("			Connection")))
				if SR.getInstance().checkInfo() == 0:
					self["statuspic"].setPixmapNum(0)
				else:
					self["statuspic"].setPixmapNum(1)
				self["statuspic"].show()

		self["list"] = List(self.list)
		self["config"].list = self.list
		self["config"].l.setList(self.list)
		self.SelectionChanged()
			
	def confirm(self, confirmed):
		if not confirmed:
			print "not confirmed"
			return
		else:
			if self.enableConfigEntry.value is True:
				SR.getInstance().modeOn()
			else:
				SR.getInstance().modeOff()
#			self.keySave()
			self.close()

			from enigma import quitMainloop
			from Screens.Standby import QuitMainloopScreen

			self.quitScreen = self.session.instantiateDialog(QuitMainloopScreen, retvalue=2)
			self.quitScreen.show()
			quitMainloop(2)

	def apply(self):
		if self.enableConfigEntry.value is True:
			self.session.openWithCallback(self.confirm, MessageBox, _("Are you sure activating LAN Setting function?"), MessageBox.TYPE_YESNO, timeout = 20, default = True)
		else:
			self.session.openWithCallback(self.confirm, MessageBox, _("Are you sure deactivating LAN Setting function?"), MessageBox.TYPE_YESNO, timeout = 20, default = True)
	
	def cancelConfirm(self, result):
		if not result:
			return
		for x in self["config"].list:
			x(1).cancel()
		self.close()

	def keyCancel(self):
		self.close()
	
	def closeRecursive(self):
		self.close(True)
	
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

	def downloadKey(self):
		if SR.getInstance().downloadInfo() < 0:
			self.session.open(MessageBox, _("Failed to download."), MessageBox.TYPE_ERROR, timeout = 7)
		else:
			self.session.open(MessageBox, _("Key downloaded."), MessageBox.TYPE_INFO, timeout = 7)


	def buildListEntry(self, Description, image):
		return((icon, description))
