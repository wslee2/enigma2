from enigma import eDVBResourceManager, Misc_Options
from Tools.Directories import fileExists, fileCheck
from Tools.HardwareInfo import HardwareInfo

SystemInfo = { }

#FIXMEE...
def getNumVideoDecoders():
	idx = 0
	while fileExists("/dev/dvb/adapter0/video%d"%(idx), 'f'):
		idx += 1
	return idx

SystemInfo["NumVideoDecoders"] = getNumVideoDecoders()
SystemInfo["PIPAvailable"] = SystemInfo["NumVideoDecoders"] > 1
SystemInfo["CanMeasureFrontendInputPower"] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()


def countFrontpanelLEDs():
	leds = 0
	if fileExists("/proc/stb/fp/led_set_pattern"):
		leds += 1

	while fileExists("/proc/stb/fp/led%d_pattern" % leds):
		leds += 1

	return leds

SystemInfo["12V_Output"] = Misc_Options.getInstance().detected_12V_output()
SystemInfo["ZapMode"] = fileCheck("/proc/stb/video/zapmode") or fileCheck("/proc/stb/video/zapping_mode")
SystemInfo["NumFrontpanelLEDs"] = countFrontpanelLEDs()
# [ IQON : micom divide for model : by knuth
#SystemInfo["FrontpanelDisplay"] = fileExists("/dev/dbox/oled0") or fileExists("/dev/dbox/lcd0")
SystemInfo["FrontpanelDisplay"] = HardwareInfo().has_micom()
# IQON : by knuth
SystemInfo["FrontpanelDisplayGrayscale"] = fileExists("/dev/dbox/oled0")
# [ IQON : deepstandby support for micom. : by knuth
#SystemInfo["DeepstandbySupport"] = HardwareInfo().get_device_name() != "dm800"
def isSupportDeepStandby():
	if HardwareInfo().has_micom():
		FP_IOCTL_SUPPORT_DEEP_STANDBY = 0x429
		fp = open('/dev/fp0', 'w')
		import fcntl
		return fcntl.ioctl(fp.fileno(), FP_IOCTL_SUPPORT_DEEP_STANDBY)
SystemInfo["DeepstandbySupport"] = isSupportDeepStandby()
from enigma import eDVBCIInterfaces
SystemInfo["NumCiSlots"] = eDVBCIInterfaces.getInstance().getNumOfSlots()
# IQON : by knuth ]

SystemInfo["Fan"] = fileCheck("/proc/stb/fp/fan")
SystemInfo["FanPWM"] = SystemInfo["Fan"] and fileCheck("/proc/stb/fp/fan_pwm")
SystemInfo["StandbyLED"] = fileCheck("/proc/stb/power/standbyled")
SystemInfo["WakeOnLAN"] = fileCheck("/proc/stb/power/wol") or fileCheck("/proc/stb/fp/wol")
SystemInfo["HasExternalPIP"] = not HardwareInfo().get_device_model().startswith("et9") and fileCheck("/proc/stb/vmpeg/1/external")
SystemInfo["VideoDestinationConfigurable"] = fileExists("/proc/stb/vmpeg/0/dst_left")
SystemInfo["hasPIPVisibleProc"] = fileCheck("/proc/stb/vmpeg/1/visible")
