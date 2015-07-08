import sys
import os
import time
from Tools.HardwareInfo import HardwareInfo

def getVersionString():
	return getImageVersionString()

def getImageVersionString():
	try:
		if os.path.isfile('/var/lib/opkg/status'):
			st = os.stat('/var/lib/opkg/status')
		else:
			st = os.stat('/usr/lib/ipkg/status')
		tm = time.localtime(st.st_mtime)
		if tm.tm_year >= 2011:
			# [ IQON : by LeeWS : %Y-%m-%d -> %m-%d-%Y
			return time.strftime("%d-%m-%Y %H:%M:%S", tm)
			# IQON ] : by LeeWS
	except:
		pass
	return _("unavailable")

def getEnigmaVersionString():
	import enigma
	enigma_version = enigma.getEnigmaVersionString()
	if '-(no branch)' in enigma_version:
		enigma_version = enigma_version [:-12]
	# [ IQON : by LeeWS : return enigma_version is replaced to below 2 lines.
	list = enigma_version.split("-")
	return list[0] + "-" + list[1] + "-" + list[2]
	# IQON ] : by LeeWS

def getKernelVersionString():
	try:
		return open("/proc/version","r").read().split(' ', 4)[2].split('-',2)[0]
	except:
		return _("unknown")

def getHardwareTypeString():
	return HardwareInfo().get_device_string()

def getBrandString():
	try:
		return open("/etc/.brandtype","r").read()
	except:
		return _("unknown")

# [ IQON : by knuth
def getHardwareModelString():
	return open("/proc/stb/info/modelname","r").read()

def getMacAddressString(ifname):
	import fcntl, socket, struct
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', ifname[:15]))
	return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

def getMicomVersionString():
	try:
		import fcntl, array
		f = array.array('h', [0])
		fp = open('/dev/dbox/fp0', 'w')
		fcntl.ioctl(fp.fileno(), 0x428, f, 1)
		return '%s' % f.tolist()[0]
	except:
		return _("unknown")

# IQON] : by knuth
def getChipSetString():
	try:
		f = open('/proc/stb/info/chipset', 'r')
		chipset = f.read()
		f.close()
		return str(chipset.lower().replace('\n','').replace('bcm',''))
	except IOError:
		return "unavailable"

def getCPUSpeedString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("cpu MHz"):
					mhz = float(splitted[1].split(' ')[0])
					if mhz and mhz >= 1000:
						mhz = "%s GHz" % str(round(mhz/1000,1))
					else:
						mhz = "%s MHz" % str(round(mhz,1))
		file.close()
		return mhz 
	except IOError:
		return "unavailable"

def getCPUString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("system type"):
					system = splitted[1].split(' ')[0]
		file.close()
		return system
	except IOError:
		return "unavailable"

def getCpuCoresString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("processor"):
					if int(splitted[1]) > 0:
						cores = 2
					else:
						cores = 1
		file.close()
		return cores
	except IOError:
		return "unavailable"

def getImageTypeString():
	try:
		return open("/etc/issue").readlines()[-2].capitalize().strip()[:-6]
	except:
		pass
	return _("undefined")

# For modules that do "from About import about"
about = sys.modules[__name__]
