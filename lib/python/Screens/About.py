from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Components.ScrollLabel import ScrollLabel
from Components.Button import Button
from Tools.HardwareInfo import HardwareInfo # [ IQON by knuth

from Tools.StbHardware import getFPVersion
from enigma import eTimer
from os import path as os_path

class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)

		# [ IQON : by knuth
		model = HardwareInfo().get_device_name() 
		macaddress = about.getMacAddressString("eth0")

		if model in ("force2solid"):
			AboutText = _("BRAND: ") + "IQON" + "\n"
			AboutText += _("Hardware: ") + "FORCE2" + "\n"
		elif model in ("tmnanose"):
			AboutText = _("Hardware: ") + "TM-NANO-SE" + "\n"
		elif model in ("optimussosplus"):
			AboutText = _("Hardware: ") + "OPTIMUSS OS+" + "\n"
		elif model in ("force2plus"):
			AboutText = _("Hardware: ") + "FORCE2+" + "\n"
		elif model in ("tmnanosecombo"):
			AboutText = _("Hardware: ") + "TM-NANO-SE Combo" + "\n"
		elif model in ("tmnanosem2"):
			AboutText = _("Hardware: ") + "TM-NANO-SE M2" + "\n"
		elif model in ("optimussos2"):
			AboutText = _("Hardware: ") + "OPTIMUSS OS2" + "\n"
		elif model in ("optimussos1"):
			AboutText = _("Hardware: ") + "OPTIMUSS OS1" + "\n"
		elif model in ("optimussos2plus"):
			AboutText = _("Hardware: ") + "OPTIMUSS OS2+" + "\n"
		elif model in ("optimussos1plus"):
			AboutText = _("Hardware: ") + "OPTIMUSS OS1+" + "\n"
		elif model in ("force2eco"):
			AboutText = _("Hardware: ") + "FORCE2 Eco" + "\n"
		elif model in ("fusionhd"):
			AboutText = _("Hardware: ") + "FUSION HD" + "\n"
		elif model in ("force1plus"):
			f = open("/etc/.brandtype", 'r')
			line = f.readline()
			if "technomate" in line:
				AboutText = _("Hardware: ") + "TM-NANO-3T COMBO" + "\n"
			elif "edision" in line:
				AboutText = _("Hardware: ") + "OPTIMUSS OS3+" + "\n"
			elif "iqon" in line:
				AboutText = _("BRAND: ") + "IQON" + "\n"
				AboutText += _("Hardware: ") + about.getHardwareTypeString() + "\n"
			else:
				AboutText = _("Hardware: ") + about.getHardwareModelString() + "\n"
			f.close()
		else:
			AboutText = _("Hardware: ") + about.getHardwareModelString() + "\n"

		AboutText += _("Mac Address: ") + macaddress + "\n"
		if HardwareInfo().has_micom():
			AboutText += _("Micom Version: ") + about.getMicomVersionString() + "\n"
#		AboutText = _("Hardware: ") + about.getHardwareTypeString() + "\n"
		AboutText += _("Image: ") + about.getImageTypeString() + "\n"
		AboutText += _("Kernel version: ") + about.getKernelVersionString() + "\n"

		EnigmaVersion = "Enigma: " + about.getEnigmaVersionString()
		self["EnigmaVersion"] = StaticText(EnigmaVersion)
		AboutText += EnigmaVersion + "\n"

		ImageVersion = _("Last upgrade: ") + about.getImageVersionString()
		self["ImageVersion"] = StaticText(ImageVersion)
		AboutText += ImageVersion + "\n"

		fp_version = getFPVersion()
		if fp_version is None:
			fp_version = ""
		else:
			fp_version = _("Frontprocessor version: %d") % fp_version
			AboutText += fp_version + "\n"

#        if path.exists('/proc/stb/info/chipset'):
		AboutText += _("Chipset: BCM%s\n") % about.getChipSetString()
		AboutText += _("CPU: %s\n") % about.getCPUString()
		AboutText += _("CPU Speed: %s\n") % about.getCPUSpeedString()
		AboutText += _("Cores: %s\n") % about.getCpuCoresString()

		self["FPVersion"] = StaticText(fp_version)

		self["TunerHeader"] = StaticText(_("Detected NIMs:"))
		AboutText += "\n" + _("Detected NIMs:") + "\n"

		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if count < 4:
				self["Tuner" + str(count)] = StaticText(nims[count])
			else:
				self["Tuner" + str(count)] = StaticText("")
			AboutText += nims[count] + "\n"

		self["HDDHeader"] = StaticText(_("Detected HDD:"))
		AboutText += "\n" + _("Detected HDD:") + "\n"

		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				if hddinfo:
					hddinfo += "\n"
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					hddinfo += "%s\n(%s, %d GB %s)" % (hdd.model(), hdd.capacity(), hdd.free()/1024, _("free"))
				else:
					hddinfo += "%s\n(%s, %d MB %s)" % (hdd.model(), hdd.capacity(), hdd.free(), _("free"))
		else:
			hddinfo = _("none")
		self["hddA"] = StaticText(hddinfo)
		AboutText += hddinfo
		self["AboutScrollLabel"] = ScrollLabel(AboutText)
		self["key_green"] = Button(_("Translations"))
		self["key_red"] = Button(_("Latest Commits"))

		self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"red": self.showCommits,
				"green": self.showTranslationInfo,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

		self["hidden_action"] = ActionMap(["ColorActions"],
		{
			"red": self.red_action,
			"blue": self.blue_action,
			"info": self.info_action,
			"1": self.first_action,
			"2": self.second_action,
			"3": self.third_action,
		},-1)

		self.key_status = -1

	def red_action(self):
		if self.key_status == 1:
			self.key_status = 2
		else:
			self.key_status = -1

	def blue_action(self):
		if self.key_status == 2:
			from Screens.ChangeRCU import ChangeRCU
			self.session.open(ChangeRCU)
			self.close()
		else:
			self.key_status = 1

	def info_action(self):
		model = HardwareInfo().get_device_name() 
		
		if self.key_status == 1:
			self.key_status = 2
			print "info_action two"
		else:
			self.key_status = 1
			print "info_action one"

	def first_action(self):
		if self.key_status == 2:
			self.key_status = 3
			print "first_action"
		else:
			self.key_status = -1
	
	def second_action(self):
		if self.key_status == 3:
			print "second_action"
			self.key_status = 4
		else:
			self.key_status = -1 

	def third_action(self):
		print "Not Using Current"
#		if self.key_status == 4:
#			print "third_action"
#                        if os_path.exists("/etc/factory"):
#                                return
#                        else:
#                                from Screens.ModeSetup import Mode4DSSetup 
#                                self.session.open(Mode4DSSetup)
#                                self.close()
#		else:
#			self.key_status == -1

	def showTranslationInfo(self):
		self.session.open(TranslationInfo)

	def showCommits(self):
		self.session.open(CommitInfo)

class TranslationInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		# don't remove the string out of the _(), or it can't be "translated" anymore.

		# TRANSLATORS: Add here whatever should be shown in the "translator" about screen, up to 6 lines (use \n for newline)
		info = _("TRANSLATOR_INFO")

		if info == "TRANSLATOR_INFO":
			info = "(N/A)"

		infolines = _("").split("\n")
		infomap = {}
		for x in infolines:
			l = x.split(': ')
			if len(l) != 2:
				continue
			(type, value) = l
			infomap[type] = value
		print infomap

		self["TranslationInfo"] = StaticText(info)

		translator_name = infomap.get("Language-Team", "none")
		if translator_name == "none":
			translator_name = infomap.get("Last-Translator", "")

		self["TranslatorName"] = StaticText(translator_name)

		self["actions"] = ActionMap(["SetupActions"],
			{
				"cancel": self.close,
				"ok": self.close,
			})

class CommitInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = ["CommitInfo", "About"]
		self["AboutScrollLabel"] = ScrollLabel(_("Please wait"))

		self["actions"] = ActionMap(["SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown,
				"left": self.left,
				"right": self.right
			})

		self.project = 0
		self.projects = [
			("enigma2", "Enigma2"),
			("openpli-oe-core", "Openpli Oe Core"),
			("enigma2-plugins", "Enigma2 Plugins"),
			("aio-grab", "Aio Grab"),
			("gst-plugin-dvbmediasink", "Gst Plugin Dvbmediasink"),
			("openembedded", "Openembedded"),
			("plugin-xmltvimport", "Plugin Xmltvimport"),
			("plugins-enigma2", "Plugins Enigma2"),
			("skin-magic", "Skin Magic"),
			("tuxtxt", "Tuxtxt")
		]
		self.cachedProjects = {}
		self.Timer = eTimer()
		self.Timer.callback.append(self.readCommitLogs)
		self.Timer.start(50, True)

	def readCommitLogs(self):
		url = 'http://sourceforge.net/p/openpli/%s/feed' % self.projects[self.project][0]
		commitlog = ""
		from urllib2 import urlopen
		try:
			commitlog += 80 * '-' + '\n'
			commitlog += url.split('/')[-2] + '\n'
			commitlog += 80 * '-' + '\n'
			for x in  urlopen(url, timeout=5).read().split('<title>')[2:]:
				for y in x.split("><"):
					if '</title' in y:
						title = y[:-7]
					if '</dc:creator' in y:
						creator = y.split('>')[1].split('<')[0]
					if '</pubDate' in y:
						date = y.split('>')[1].split('<')[0][:-6]
				commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'
			self.cachedProjects[self.projects[self.project][1]] = commitlog
		except:
			commitlog = _("Currently the commit log cannot be retrieved - please try later again")
		self["AboutScrollLabel"].setText(commitlog)

	def updateCommitLogs(self):
		if self.cachedProjects.has_key(self.projects[self.project][1]):
			self["AboutScrollLabel"].setText(self.cachedProjects[self.projects[self.project][1]])
		else:
			self["AboutScrollLabel"].setText(_("Please wait"))
			self.Timer.start(50, True)

	def left(self):
		self.project = self.project == 0 and len(self.projects) - 1 or self.project - 1
		self.updateCommitLogs()

	def right(self):
		self.project = self.project != len(self.projects) - 1 and self.project + 1 or 0
		self.updateCommitLogs()
