import os
from Tools.Directories import SCOPE_SKIN, resolveFilename

hw_info = None

class HardwareInfo:
	device_name = _("unavailable")
	device_model = None
	device_version = ""
	device_revision = ""
	device_hdmi = False

	def __init__(self):
                global hw_info
		if hw_info is not None:
#			print "using cached result"
			return
		hw_info = self

		print "Scanning hardware info"
		# Version
		if os.path.exists("/proc/stb/info/version"):
			self.device_version = open("/proc/stb/info/version").read().strip()
		# Revision
		if os.path.exists("/proc/stb/info/board_revision"):
			self.device_revision = open("/proc/stb/info/board_revision").read().strip()

		# Name ... bit odd, but history prevails
		# if os.path.exists("/proc/stb/info/model"):
		# 	self.device_name = open("/proc/stb/info/model").read().strip()
		# elif os.path.exists("/proc/stb/info/hwmodel"):
		#	self.device_name = open("/proc/stb/info/hwmodel").read().strip()
# [ IQON : by LeeWS : our model is inserted  at /proc/stb/info/hwmodel, This should be checked first. 
		if os.path.exists("/proc/stb/info/hwmodel"):
			self.device_name = open("/proc/stb/info/hwmodel").read().strip()
# IQON ] : by LeeWS
		else:
			print "----------------"
			print "you should upgrade to new drivers for the hardware detection to work properly"
			print "----------------"
			print "fallback to detect hardware via /proc/cpuinfo!!"
			try:
				rd = open("/proc/cpuinfo", "r").read()
				if "Brcm4380 V4.2" in rd:
					self.device_name = "dm8000"
				elif "Brcm7401 V0.0" in rd:
					self.device_name = "dm800"
				elif "MIPS 4KEc V4.8" in rd:
					self.device_name = "dm7025"
				rd.close();
			except:
				pass

		# Model
		for line in open((resolveFilename(SCOPE_SKIN, 'hw_info/hw_info.cfg')), 'r'):
			if not line.startswith('#') and not line.isspace():
				l = line.strip().replace('\t', ' ')
				if l.find(' ') != -1:
					infoFname, prefix = l.split()
				else:
					infoFname = l
					prefix = ""
				if os.path.exists("/proc/stb/info/" + infoFname):
					self.device_model = prefix + open("/proc/stb/info/" + infoFname).read().strip()
					break

		if self.device_model is None:
			self.device_model = self.device_name

		# HDMI capbility
		self.device_hdmi = (	self.device_name == 'dm7020hd' or
					self.device_name == 'dm800se' or
					self.device_name == 'dm500hd' or
					(self.device_name == 'dm8000' and self.device_version != None))

		print "Detected: " + self.get_device_string()


	def get_device_name(self):
		return hw_info.device_name

	def get_device_model(self):
		return hw_info.device_model

	def get_device_version(self):
		return hw_info.device_version

	def get_device_revision(self):
		return hw_info.device_revision

	def get_device_string(self):
		s = hw_info.device_model
		if hw_info.device_revision != "":
			s += " (" + hw_info.device_revision + "-" + hw_info.device_version + ")"
		elif hw_info.device_version != "":
			s += " (" + hw_info.device_version + ")"
		return s

	def has_hdmi(self):
	# [ IQON : by LeeWS : replace from return hw_info.device_hdmi because display to "DVI" at initial menu
		DEVICES_WITHOUT_HDMI = []
		if self.get_device_model() in DEVICES_WITHOUT_HDMI:
			return False
		else:
			return True
	# IQON ] : by LeeWS

	#[ IQON by knuth
	# HardwareInfo().device_name instead to get_device_model function.

	def has_micom(self):
		DEVICES_WITHOUT_MICOM = []
		if self.get_device_model() in DEVICES_WITHOUT_MICOM:
			return False
		else:
			return True
	
	def has_vcr(self):
		DEVICES_WITH_VCR = [ "tmtwinoe", "ios100hd" ]
		if self.get_device_model() in DEVICES_WITH_VCR:
			return False
		else:
			return True
	
	def has_yuv(self):
		DEVICES_WITH_YUV = [ 'force1', 'tmtwinoe', 'ios100hd', 'ios200hd', 'tmnano2t', 'optimussos2', 'optimussos2plus' ]
		if self.get_device_model() in DEVICES_WITH_YUV:
			return True
		else:
			return False

	def support_1080p_50_60(self):
		DEVICES_WITH_1080P_50_60 = [ 'force1', 'tmnanosuper', 'tm2tsuper', 'force1plus', 'optimussos1plus', 'optimussos2plus', 'tmnano2super', 'force2solid', 'force2', 'tmnanose', 'optimussosplus', 'force2plus', 'tmnanosecombo', 'tmnanosem2', 'force2eco', 'fusionhd' ]
		if self.get_device_model() in DEVICES_WITH_1080P_50_60:
			return True
		else:
			return False

	def has_scart(self):
		DEVICES_WITH_SCART = [ 'tmtwinoe', 'ios100hd', 'tm2toe', 'tmsingle', 'ios300hd', 'mediabox'  ]
		if self.get_device_model() in DEVICES_WITH_SCART:
			return True
		else:
			return False
	#IQON ] by knuth
