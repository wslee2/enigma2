from Components.Pixmap import MovingPixmap, MultiPixmap
from Tools.Directories import resolveFilename, SCOPE_SKIN
from xml.etree.ElementTree import ElementTree
from Components.config import config, ConfigInteger
from Components.RcModel import rc_model

config.misc.rcused = ConfigInteger(default = 1)

class Rc:
	def __init__(self):
		self["rc"] = MultiPixmap()
		self["arrowdown"] = MovingPixmap()
		self["arrowdown2"] = MovingPixmap()
		self["arrowup"] = MovingPixmap()
		self["arrowup2"] = MovingPixmap()

		config.misc.rcused = ConfigInteger(default = 1)
		self.isDefaultRc = rc_model.rcIsDefault()
		self.rcheight = 500
		self.rcheighthalf = 250

		self.selectpics = []
#		self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-18,-70)))
#		self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-18,0)))
# [ IQON : by LeeWS : replace below list from upper 2 lines.
		from Tools.HardwareInfo import HardwareInfo
		if HardwareInfo().get_device_name() in ('twin', 'tm2toe' , '2t', 'tmtwinoe' , 'tmsingle', 'tmsinglemini', 'tmnanooe', 'tmnano2t', 'tm2tsuper', 'tmnanosuper', 'tmnano2super' ):
			self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-23,-98)))
			self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-23,0)))
		if HardwareInfo().get_device_name() in ('ios100hd', 'ios200hd' , 'ios300hd' , 'mediabox', 'optimussos1', 'optimussos2', 'force1', 'optimussos1plus', 'optimussos2plus', 'force1plus', 'force2', 'force2solid', 'tmnanose', 'optimussosplus', 'force2plus', 'tmnanosecombo', 'tmnanosem2', 'force2eco', 'fusionhd'):
			if HardwareInfo().get_device_name() == "force1plus":
				# f = open("/etc/.brandtype", 'r')
				# line = f.readline()
				# if "technomate" in line:
				#	self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-23,-98)))
				#	self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-23,0)))
				# else:
				#	self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-23,-125)))
				#	self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-22,-45)))
				# f.close()
				self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-23,-125)))
				self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-22,-45)))
			else:
				self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-23,-125)))
				self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-22,-45)))
		else:
			self.selectpics.append((self.rcheighthalf, ["arrowdown", "arrowdown2"], (-18,-70)))
			self.selectpics.append((self.rcheight, ["arrowup", "arrowup2"], (-18,-0)))
# IQON ] : by LeeWS

		self.readPositions()
		self.clearSelectedKeys()
		self.onShown.append(self.initRc)

	def initRc(self):
		if self.isDefaultRc:
			self["rc"].setPixmapNum(config.misc.rcused.value)
		else:
			self["rc"].setPixmapNum(0)

	def readPositions(self):
		if self.isDefaultRc:
			target = resolveFilename(SCOPE_SKIN, "rcpositions.xml")
		else:
			target = rc_model.getRcPositions()
		tree = ElementTree(file = target)
		rcs = tree.getroot()
		self.rcs = {}
		for rc in rcs:
			id = int(rc.attrib["id"])
			self.rcs[id] = {}
			for key in rc:
				name = key.attrib["name"]
				pos = key.attrib["pos"].split(",")
				self.rcs[id][name] = (int(pos[0]), int(pos[1]))

	def getSelectPic(self, pos):
		for selectPic in self.selectpics:
			if pos[1] <= selectPic[0]:
				return (selectPic[1], selectPic[2])
		return None

	def hideRc(self):
		self["rc"].hide()
		self.hideSelectPics()

	def showRc(self):
		self["rc"].show()

	def selectKey(self, key):
		if self.isDefaultRc:
			rc = self.rcs[config.misc.rcused.value]
		else:
			rc = self.rcs[2]
		if rc.has_key(key):
			rcpos = self["rc"].getPosition()
			pos = rc[key]
			selectPics = self.getSelectPic(pos)
			selectPic = None
			for x in selectPics[0]:
				if x not in self.selectedKeys:
					selectPic = x
					break
			if selectPic is not None:
				print "selectPic:", selectPic
				self[selectPic].moveTo(rcpos[0] + pos[0] + selectPics[1][0], rcpos[1] + pos[1] + selectPics[1][1], 1)
				self[selectPic].startMoving()
				self[selectPic].show()
				self.selectedKeys.append(selectPic)

	def clearSelectedKeys(self):
		self.showRc()
		self.selectedKeys = []
		self.hideSelectPics()

	def hideSelectPics(self):
		for selectPic in self.selectpics:
			for pic in selectPic[1]:
				self[pic].hide()
