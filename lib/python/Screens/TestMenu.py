from Screen import Screen
from Components.ChoiceList import ChoiceEntryComponent, ChoiceList
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Label import MultiColorLabel, Label
from Components.config import ConfigIP, NoSave, configfile, config, Config, ConfigSubsection
from Components.Network import iNetwork
from Components.Console import Console
from Components.Harddisk import harddiskmanager
from Components.About import about
from Components.FanControl import fancontrol
from Components.Sensors import sensors
from Components.Sources.Sensor import SensorSource
from Components.NimManager import nimmanager, InitNimManager
from Tools.HardwareInfo import HardwareInfo
from Screens.MessageBox import MessageBox
from Screens.Standby import QuitMainloopScreen
from Plugins.SystemPlugins.Videomode.VideoHardware import video_hw
from enigma import eTimer, eServiceReference, eDVBDB, quitMainloop
from enigma import eDVBResourceManager, iDVBFrontend
from enigma import eDVBCI_UI, eDVBCIInterfaces
from enigma import eDVBVolumecontrol
import os, fcntl, array, socket, struct

class TestMenu(Screen):
# 1.0.0	- 
# 1.0.1 - alpumr check removed
# 1.0.2 - optimussos1, optimussos2 model added.
# 1.0.3 - de language update.
# 1.0.4 - optimussos1plus, optimussos2plus model added.
# 1.0.5 - Smart Card N/A problem
# 1.0.6 - 7362 model test menu modified.
# 1.0.7 - force2 model test menu.

	TEST_PROG_VERSION = "1.0.7"
	skin = """
        <screen name="TestMenu" position="fill" title="Test Menu" flags="wfNoBorder">
			<eLabel position="fill" backgroundColor="transpBlack" zPosition="-50"/>

			<widget name="label0"		position="80,55"	size="540,29"	foregroundColor="#0006c8f3" backgroundColor="#40000000" font="Regular;22" zPosition="1" />

			<widget name="menulist"		position="80,90"	size="540,250"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22"  zPosition="1" backgroundColorSelected="white" foregroundColorSelected="black" />

			<widget name="lan_i"		position="80,350"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="sc0_i"		position="80,380"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="sc1_i"		position="80,410"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="ci0_i"		position="80,440"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="ci1_i"		position="80,470"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="sata_i"		position="80,500"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="usb0_i"		position="80,530"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="usb1_i"		position="80,560"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="usb2_i"		position="80,590"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />

			<widget name="lan_s"		position="280,350"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="sc0_s"		position="280,380"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="sc1_s"		position="280,410"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="ci0_s"		position="280,440"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="ci1_s"		position="280,470"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="sata_s"		position="280,500"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="usb0_s"		position="280,530"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="usb1_s"		position="280,560"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="usb2_s"		position="280,590"	size="340,29"	foregroundColors="#00ff4500,#007fff00" backgroundColor="#40000000" font="Regular;22" zPosition="1" />

			<widget name="label1"		position="640,055"	size="540,29"	foregroundColor="#0006c8f3" backgroundColor="#40000000" font="Regular;22" zPosition="1" />

			<widget name="mac_i"		position="640,090"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="info0_i"		position="640,120"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="info1_i"		position="640,150"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="micom_i"		position="640,180"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="security0_i"	position="640,210"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="security1_i"	position="640,240"	size="199,29"	foregroundColor="white" backgroundColor="#40000000" font="Regular;22" zPosition="1" />

			<widget name="mac_s"		position="840,090"	size="340,29"	foregroundColors="white,#00ff4500" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="info0_s"		position="840,120"	size="340,29"	foregroundColors="white,#00ff4500" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="info1_s"		position="840,150"	size="340,29"	foregroundColors="white,#00ff4500" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="micom_s"		position="840,180"	size="340,29"	foregroundColors="white,#00ff4500" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="security0_s"	position="840,210"	size="340,29"	foregroundColors="white,#00ff4500" backgroundColor="#40000000" font="Regular;22" zPosition="1" />
			<widget name="security1_s"	position="840,240"	size="340,29"	foregroundColors="white,#00ff4500" backgroundColor="#40000000" font="Regular;22" zPosition="1" />

			<widget name="button_left"		position="840,430"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_right"		position="925,430"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_down"		position="1010,430"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_up"		position="1095,430"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_power"		position="840,450"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_menu"		position="925,450"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_ok"		position="1010,450"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_exit"		position="1095,450"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />
			<widget name="button_info"		position="840,480"	size="84,19"	foregroundColors="#00ff4500,#0070ff00" backgroundColor="#40000000" font="Regular;18" zPosition="1" halign="center" />

			<eLabel name="snr" position="840,350" size="340,19" halign="left" transparent="1" text="SNR" font="Regular;18" />
			<widget source="session.FrontendStatus" render="Progress" pixmap="PLi-HD/infobar/pbar_grey.png" backgroundColor="#40000000" position="840,350" size="340,19" >
				<convert type="FrontendInfo">SNR</convert>
			</widget>
			<widget source="session.FrontendStatus" render="Label" position="840,350" size="340,19" backgroundColor="#40000000" transparent="1" halign="right" font="Regular;18" >
				<convert type="FrontendInfo">SNR</convert>
			</widget>
			<eLabel name="agc" position="840,370" size="84,19" backgroundColor="#40000000" halign="left" text="AGC" font="Regular;18" />
			<widget source="session.FrontendStatus" render="Label" position="925,370" size="84,19" backgroundColor="#40000000" font="Regular;18">
			  <convert type="FrontendInfo">AGC</convert>
			</widget>
			<eLabel name="ber" position="1011,370" size="84,19" backgroundColor="#40000000" halign="left" text="BER" font="Regular;18" />
			<widget source="session.FrontendStatus" render="Label" position="1096,370" size="84,19" backgroundColor="#40000000" font="Regular;18">
			  <convert type="FrontendInfo">BER</convert>
			</widget>

			<widget source="SensorFanText0" render="Label" position="840,400" size="84,19" font="Regular;18" backgroundColor="#40000000" />
			<widget source="SensorFan0" render="Label" position="925,400" size="84,19" font="Regular;18" backgroundColor="#40000000" >
				<convert type="SensorToText"></convert>
			</widget>
			<widget source="SensorTempText0" render="Label" position="1011,400" size="84,19" font="Regular;18" backgroundColor="#40000000" />
			<widget source="SensorTemp0" render="Label" position="1096,400" size="84,19" font="Regular;18" backgroundColor="#40000000" >
				<convert type="SensorToText"></convert>
			</widget>
        </screen>"""

	CARD_LIST = {
		chr(0x3b) + chr(0x9f) + chr(0x21) + chr(0x0e) + chr(0x49) + chr(0x52) + chr(0x44) : "Irdeto",
		chr(0x3b) + chr(0xf7) + chr(0x11) + chr(0x00) : "Seca",
		chr(0x3b) + chr(0x78) + chr(0x12) : "Cryptoworks", 
		chr(0x3b) + chr(0x26) + chr(0x00) : "Conax", 
		chr(0x3b) + chr(0x24) + chr(0x00) : "Conax", 
		chr(0x3b) + chr(0x34) + chr(0xd6) : "Drecrypt", 
		chr(0x3f) + chr(0xff) + chr(0x95) : "Nagravision", 
		chr(0x3f) + chr(0x7f) + chr(0x13) : "NDS", 
		chr(0x3f) + chr(0xfd) + chr(0x13) : "NDS", 
		chr(0x3f) + chr(0x27) + chr(0x17) : "Viaccess", 
		chr(0x3f) + chr(0x77) + chr(0x18) : "Viaccess", 
		chr(0x3b) + chr(0x77) + chr(0x18) : "Viaccess", 
		chr(0x3b) + chr(0x9c) + chr(0x13) + chr(0x11) + chr(0x81) + chr(0x64) + chr(0x72) : "Firecrypt", 
		chr(0x3b) + chr(0xec) + chr(0x00) + chr(0x00) + chr(0x40) + chr(0x38) + chr(0x57) : "Type1", 
		chr(0x3b) + chr(0xff) + chr(0xe0) + chr(0x1c) + chr(0x57) + chr(0xe0) + chr(0x74) : "Type2",
		chr(0x3f) + chr(0xfd) + chr(0x95) + chr(0x00) + chr(0xff) + chr(0x91) + chr(0x81) : "Type3"} 

	# 0 - front, 1 - upper rear, 2 - lower rear
	USBDB = {
		"tmtwinoe":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"tm2toe":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"tmsingle":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"tmnanooe":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"ios100hd":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"ios200hd":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"ios300hd":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"mediabox":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"optimussos1":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"optimussos2":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"optimussos1plus":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0,
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 2,
		},
		"optimussos2plus":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0,
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 2,
		},
		"tmnano2t":
		{
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 0,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-1:1.0": 2,
		},
		"tmnano2super":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0,
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 2,
		},
		"force1":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0,
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 2,
			},
		"force1plus":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0,
			"/devices/platform/ehci-brcm.1/usb2/2-1/2-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 2,
		},
		"force2":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-0:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-1:1.0": 2,
		},
		"force2solid":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"tmnanose":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"optimussosplus":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"force2plus":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"tmnanosecombo":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"tmnanosem2":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"force2eco":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		},
		"fusionhd":
		{
			"/devices/platform/ehci-brcm.2/usb3/3-1/3-1:1.0": 0, # DUMMY
			"/devices/platform/ehci-brcm.0/usb1/1-1/1-1:1.0": 1,
			"/devices/platform/ehci-brcm.0/usb1/1-2/1-2:1.0": 2,
		}
		}

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session

		if HardwareInfo().get_device_name() == "mediabox":
			os.system("opkg remove enigma2-plugin-channel.non.motorized-techsat-17-29-57")
		os.system("rm /etc/enigma2 -rf; touch /etc/.run_factory_test; tar xf /etc/.e2settings.tar -C /")
		configfile.load()
		nimmanager.readTransponders()
		InitNimManager(nimmanager)
		eDVBDB.getInstance().reloadBouquets()
		eDVBDB.getInstance().reloadServicelist()

		self.iface = "eth0"

		self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions", "InfobarChannelSelection", "StandbyActions", "GlobalActions", "TimerEditActions"], 
				{
				"ok": self.go,
				"back": self.cancel,
				"up": self.up,
				"down": self.down,
				"1": self.keyNumberGlobal,
				"2": self.keyNumberGlobal,
				"3": self.keyNumberGlobal,
				"4": self.keyNumberGlobal,
				"5": self.keyNumberGlobal,
				"6": self.keyNumberGlobal,
				"7": self.keyNumberGlobal,
				"8": self.keyNumberGlobal,
				"9": self.keyNumberGlobal,
				"0": self.keyNumberGlobal,
				"red": self.keyRed,
				"green": self.keyGreen,
				"yellow": self.keyYellow,
				"blue": self.keyBlue,
				"left": self.frontButtonLeft,
				"right": self.frontButtonRight,
				"exit": self.frontButtonExit,
				"menu": self.frontButtonMenu,
				"power": self.frontButtonPower,
				"ChannelPlusPressed": self.frontButtonChPlus,
				"ChannelMinusPressed": self.frontButtonChMinus,
				"keyChannelUp": self.frontButtonChPlus,
				"keyChannelDown": self.frontButtonChMinus,
				"volumeUp": self.frontButtonVolUp,
				"volumeDown": self.frontButtonVolDown,
				"log": self.frontButtonInfo,
				}, -1)

		model = HardwareInfo().get_device_name()
		brandtype = open("/etc/.brandtype","r").readline()

		self.has_fan = model not in ("mediabox", "force2", "tmnanose", "optimussosplus", "force2solid", "force2plus", "tmnanosecombo", "tmnanosem2", "force2eco", "fusionhd" )
		self.has_nav_keys = model not in ("tmtwinoe", "ios100hd", "mediabox", "ios200hd", "optimussos2", "optimussos2plus","force1","force1plus")
		self.has_8_buttons = model in ("tmtwinoe", "ios100hd")

		if "iqon" in brandtype:
			self.has_9_buttons = model in ("tm2toe", "tmsingle", "force1")
			self.has_5_buttons = model in ("mediabox","ios200hd", "optimussos2", "tmnano2t", "optimussos2plus", "force1plus")
		else:
			self.has_9_buttons = model in ("tm2toe", "tmsingle", "force1", "force1plus")
			self.has_5_buttons = model in ("mediabox","ios200hd", "optimussos2", "tmnano2t", "optimussos2plus")

		self.has_7_buttons = model in ("tmnanooe", "ios300hd", "optimussos1", "optimussos1plus", "tmnano2super")
		self.has_1_buttons = model in ("tmnanose", "optimussosplus", "force2", "force2solid", "force2plus", "tmnanosecombo", "tmnanosem2", "force2eco", "fusionhd") 
		self.has_fan_sensor = model in ("tmtwinoe", "tm2toe", "ios100hd", "optimussos1plus", "optimussos2plus", "tmnano2super", "force1", "force1plus")
		self.has_sata = model not in ("ios300hd", "mediabox", "tmnanose", "optimussosplus", "force2", "force2solid", "force2plus", "tmnanosecombo", "tmnanosem2", "force2eco", "fusionhd")
		self.has_front_usb = model not in ("tmnanose", "optimussosplus", "force2", "force2solid", "force2plus", "tmnanosecombo", "tmnanosem2", "force2eco", "fusionhd" )
		self.has_sc41cr = model in ("ios200hd", "optimussos1","optimussos2", "tmnano2t")
		self.has_sc50cr = model in ("tmnanooe", "optimussos1plus", "optimussos2plus", "tmnano2super", "force1", "force1plus", "tmnanose", "optimussosplus", "force2", "force2solid", "force2plus", "tmnanosecombo", "tmnanosem2", "force2eco", "fusionhd" )
		self.has_1_tuner = model in ("tmnanooe", "ios300hd", "mediabox", "tmsingle", "optimussos1", "force2", "force2solid", "tmnanose" , "optimussosplus", "tmnanosem2", "force2plus", "tmnanosecombo", "force2eco", "fusionhd" )
		self.has_vfd = model not in ("tmsingle", "tmnanooe", "ios200hd", "ios300hd", "mediabox", "optimussos1", "tmnano2t", "optimussos1plus", "tmnano2super")
		# 7362 combo model define : leews
		self.has_7362_combo = model in ("tmnanosecombo", "force2plus", "fusionhd") 

		self.MENU_LIST = []
		self.MENU_LIST.append([ "[T1] H18,  720P, CVBS, 4:3,  22OFF (RTPi)",	  "ch1",	self.func ])
		self.MENU_LIST.append([ "[T1] V14,  576i, YC,   4:3,  22OFF (DUBAI)",	"ch2",	self.func ])
		if len(nimmanager.nimList()) == 2:
			if self.has_7362_combo:
				self.MENU_LIST.append([ "[T1] H18,  576i, RGB,  16:9, 22OFF (France 24)",	"ch3",	self.func ])
				self.MENU_LIST.append([ "[T1] V14, 1080i, CVBS, 16:9, 22OFF (DUBAI SPORT3)",	"ch4",	self.func ])
				#self.MENU_LIST.append([ "[DVB-C  474MHz 6900-64QAM]  (RTE ONE)",	"ch5",	self.func ]) # Cable
				self.MENU_LIST.append([ "[DVB-T 474MHz 8M 64QAM]  BBC NEWS 24",	"ch5",	self.func ]) # Terrestrial
			else:
				self.MENU_LIST.append([ "[T2] H18,  576i, RGB,  16:9, 22OFF (France 24)",	"ch3",	self.func ])
				self.MENU_LIST.append([ "[T2] V14, 1080i, CVBS, 16:9, 22OFF (DUBAI SPORT3)",	"ch4",	self.func ])
		else:
			if len(nimmanager.nimList()) == 1:
				self.MENU_LIST.append([ "[T1] H18,  576i, RGB,  16:9, 22OFF (France 24)",	"ch3",	self.func ])
				self.MENU_LIST.append([ "[T1] V14, 1080i, CVBS, 16:9, 22OFF (DUBAI SPORT3)",	"ch4",	self.func ])
			if len(nimmanager.nimList()) == 3:
				self.MENU_LIST.append([ "[T2] H18,  576i, RGB,  16:9, 22OFF (France 24)",	"ch3",	self.func ])
				self.MENU_LIST.append([ "[T2] V14, 1080i, CVBS, 16:9, 22OFF (DUBAI SPORT3)",	"ch4",	self.func ])
				#self.MENU_LIST.append([ "[DVB-C  474MHz 6900-64QAM]  (RTE ONE)",	"ch5",	self.func ]) # Cable
				self.MENU_LIST.append([ "[DVB-T 474MHz 8M 64QAM]  BBC NEWS 24",	"ch5",	self.func ]) # Terrestrial
			
		self.MENU_LIST.append([ "22Khz	-  ON /[OFF]",							"tone",	self.func ])
		if self.has_fan:
			self.MENU_LIST.append([ "FAN	- [ON]/ OFF",								"fan",	self.func ])
		self.MENU_LIST.append([ "FRONT PANEL",										"fp",	self.func ])
		self.MENU_LIST.append([ "DEEP STANDBY",										"ds",	self.func ])

		self.BUTTON_TEST = {
			"ok":		{ "button":"button_ok",		"func":self.frontButtonOk,		"pressed":False, "text":"OK" },
			"up":		{ "button":"button_up",		"func":self.frontButtonUp,		"pressed":False, "text":"^" },
			"down":		{ "button":"button_down",	"func":self.frontButtonDown,	"pressed":False, "text":"V" },
			"left":		{ "button":"button_left",	"func":self.frontButtonLeft,	"pressed":False, "text":"<" },
			"right":	{ "button":"button_right",	"func":self.frontButtonRight,	"pressed":False, "text":">" },
			"exit":		{ "button":"button_exit",	"func":self.frontButtonExit,	"pressed":False, "text":"EXIT" },
			"menu":		{ "button":"button_menu",	"func":self.frontButtonMenu,	"pressed":False, "text":"MENU" },
			"power":	{ "button":"button_power",	"func":self.frontButtonPower,	"pressed":False, "text":"POWER" }}
		if not self.has_nav_keys:
			f = open("/etc/.brandtype", 'r')
			line = f.readline()
			if line != "worldvision":
				self.BUTTON_TEST["up"]["text"] = "VOL+"
				self.BUTTON_TEST["up"]["func"] = self.frontButtonVolUp
				self.BUTTON_TEST["down"]["text"] = "VOL-"
				self.BUTTON_TEST["down"]["func"] = self.frontButtonVolDown
				self.BUTTON_TEST["left"]["text"] = "CH-"
				self.BUTTON_TEST["left"]["func"] = self.frontButtonChMinus
				self.BUTTON_TEST["right"]["text"] = "CH+"
				self.BUTTON_TEST["right"]["func"] = self.frontButtonChPlus
			f.close()	
		if self.has_9_buttons:
			model = HardwareInfo().get_device_name() 
			f = open("/etc/.brandtype", 'r')
			line = f.readline()
			if model == "force1":
				if "worldvision" in line:
					self.BUTTON_TEST["info"] = { "button":"button_info",    "func":self.frontButtonInfo,    "pressed":False, "text":"INFO" }
				else:
					self.BUTTON_TEST.pop("exit")
					self.BUTTON_TEST.pop("menu")
					self.BUTTON_TEST.pop("ok")
			elif model == "force1plus":
				if "worldvision" in line:
					self.BUTTON_TEST["info"] = { "button":"button_info",    "func":self.frontButtonInfo,    "pressed":False, "text":"INFO" }
				else:
					self.BUTTON_TEST.pop("exit")
					self.BUTTON_TEST.pop("menu")
					self.BUTTON_TEST.pop("ok")
			else:
				self.BUTTON_TEST["info"] = { "button":"button_info",	"func":self.frontButtonInfo,	"pressed":False, "text":"INFO" }
			f.close()
			
		if self.has_7_buttons:
			self.BUTTON_TEST.pop("exit")

		if self.has_5_buttons:
			self.BUTTON_TEST.pop("exit")
			self.BUTTON_TEST.pop("menu")
			self.BUTTON_TEST.pop("ok")
			
		if self.has_1_buttons:
			self.BUTTON_TEST.pop("up")
			self.BUTTON_TEST.pop("down")
			self.BUTTON_TEST.pop("left")
			self.BUTTON_TEST.pop("right")
			self.BUTTON_TEST.pop("menu")
			self.BUTTON_TEST.pop("ok")
			self.BUTTON_TEST.pop("exit")

		self.fpTestMode = False
		self.service = "ch1"

		self.setMenuList(self.MENU_LIST)
		self.setTestItemsLabel()
	
		# models using fan ic, available rpm, temp
		if self.has_fan_sensor:
			self.initFanSensors()

		self.networkMonitor = eTimer()
		self.networkMonitor.callback.append(self.getLinkState)
		self.networkMonitor.start(1000, True)

		self.smartcardInserted = [ False, False ]
		self.smartcardMonitor = eTimer()
		self.smartcardMonitor.callback.append(self.getSCState)
		self.smartcardMonitor.start(1000, False)

		self.ciMonitor = eTimer()
		self.ciMonitor.callback.append(self.getCIState)
		self.ciMonitor.start(1000, False)

		self.storageMonitor = eTimer()
		self.storageMonitor.callback.append(self.getStorageState)
		self.storageMonitor.start(1000, False)

		self.onLayoutFinish.append(self.layoutFinished)

	def cancel(self):
		if self.fpTestMode:
			self.frontButtonExit()
#		else:
#			self.session.openWithCallback(self.quitConfirmed, MessageBox, _("Do you really want to quit?"), default = False)

	def quitConfirmed(self, answer):
		if answer:
			self.quit(3)

	def quit(self, mode):
		self.networkMonitor.stop()
		self.smartcardMonitor.stop()
		self.ciMonitor.stop()
		self.storageMonitor.stop()
		self.session.nav.stopService();  # insert channel close for system halt of 7356 models
		self.hide()
		if mode == 1:
			os.system("rm /etc/enigma2 -rf")
			self.hide()
			self.quitScreen = self.session.instantiateDialog(QuitMainloopScreen,retvalue=mode)
			self.quitScreen.show()
			quitMainloop(mode)
		elif mode == 3:
			os.system("rm /etc/.run_factory_test -f; rm /etc/enigma2 -rf")
			if HardwareInfo().get_device_name() == "mediabox":
				os.system("tar xvf /etc/var.tar -C /; opkg install /tmp/enigma2-plugin-channel.non.motorized-techsat-17-29-57_20130610_all.ipk")
			os.system("/etc/init.d/softcam start;/etc/init.d/cardserver start;killall enigma2")

	def up(self):
		if self.fpTestMode:
			self.frontButtonUp()
		else:
			if len(self["menulist"].list) > 0:
				while 1:
					self["menulist"].instance.moveSelection(self["menulist"].instance.moveUp)
					if self["menulist"].l.getCurrentSelection()[0][0] != "--" or self["menulist"].l.getCurrentSelectionIndex() == 0:
						break

				os.system("echo \"%s\" > /proc/stb/lcd/show_txt" % self["menulist"].l.getCurrentSelection()[0][0])
				self.vfdTextWrite(self["menulist"].l.getCurrentSelection()[0][0])

	def down(self):
		if self.fpTestMode:
			self.frontButtonDown()
		else:
			if len(self["menulist"].list) > 0:
				while 1:
					self["menulist"].instance.moveSelection(self["menulist"].instance.moveDown)
					if self["menulist"].l.getCurrentSelection()[0][0] != "--" or self["menulist"].l.getCurrentSelectionIndex() == len(self["menulist"].list) - 1:
						break

				os.system("echo \"%s\" > /proc/stb/lcd/show_txt" % self["menulist"].l.getCurrentSelection()[0][0])
				self.vfdTextWrite(self["menulist"].l.getCurrentSelection()[0][0])

	# runs a number shortcut
	def keyNumberGlobal(self, number):
		if self.fpTestMode:
			return
		else:
			self.goKey(str(number))

	# runs the current selected entry
	def go(self):
		if self.fpTestMode:
			self.frontButtonOk()
		else:
			cursel = self["menulist"].l.getCurrentSelection()
			if cursel:
				self.goEntry(cursel[0])
			else:
				self.cancel()

	# runs a specific entry
	def goEntry(self, entry):
# do self.func
		os.system("echo \"%s\" > /proc/stb/lcd/show_txt" % entry[0])
		self.vfdTextWrite(entry[0])

		entry[2](entry)

	# lookups a key in the keymap, then runs it
	def goKey(self, key):
		if self.keymap.has_key(key):
			self["menulist"].instance.moveSelectionTo(self.__keys.index(key))
			entry = self.keymap[key]
			self.goEntry(entry)

	# runs a color shortcut
	def keyRed(self):
		if self.fpTestMode:
			self.fpTestQuit()
		else:
			self.goKey("red")

	def keyGreen(self):
		self.goKey("green")

	def keyYellow(self):
		self.goKey("yellow")

	def keyBlue(self):
		self.goKey("blue")

# ---------------------------------------------------------------------
#  ui
# ---------------------------------------------------------------------

	def setMenuList(self, list):
		self.list = []
# 0 for exit
#		self.__keys = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "red", "green", "yellow", "blue" ] + (len(list) - 10) * [""]
		self.__keys = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "red", "green", "yellow", "blue" ] + (len(list) - 10) * [""]

		pos = 0
		self.keymap = {}
		for x in list:
			strpos = str(self.__keys[pos])
			self.list.append(ChoiceEntryComponent(key = strpos, text = x))
			if self.__keys[pos] != "":
				self.keymap[self.__keys[pos]] = list[pos]
			pos += 1

# 0 for exit, add to end of menu list
		self.keymap["0"] = [ "EXIT",	"exit",	self.func ]
		self.list.append(ChoiceEntryComponent(key = "0", text = self.keymap["0"]))
		self.__keys[pos] = "0"

		if not self.has_key("menulist"):
			self["menulist"] = ChoiceList(self.list)
		else:
			self["menulist"].hide()
			self["menulist"].setList(self.list)
		self["menulist"].show()

	def setTestItemsLabel(self):
		self["label0"] = Label(_(" TEST MENU"))
		self["label1"] = Label(_(" SYSTEM INFORMATION"))

		self["lan_i"] = Label(_(" IP"))
		self["lan_s"] = MultiColorLabel(_(" N/A"))

		self["sata_i"] = Label(_(" iSATA"))
		self["sata_s"] = MultiColorLabel(_(" N/A"))
		# not support internal sata
		if not self.has_sata:
			self["sata_i"].hide()
			self["sata_s"].hide()

		self["info0_i"] = Label(_(" Hardware"))
		self["info0_s"] = MultiColorLabel(_(" N/A"))

		self["info1_i"] = Label(_(" Version"))
		self["info1_s"] = MultiColorLabel(_(" N/A"))

		self["mac_i"] = Label(_(" Mac Address"))
		self["mac_s"] = MultiColorLabel(_(" N/A"))

		self["micom_i"] = Label(_(" Micom Version"))
		self["micom_s"] = MultiColorLabel(_(" N/A"))

		for i in (0, 1):
			self["sc%d_i" % i] = Label(_(" SC Slot-%d" % (i+1)))
			self["sc%d_s" % i] = MultiColorLabel(_(" N/A"))

			self["ci%d_i" % i] = Label(_(" CI Slot-%d" % (i+1)))
			self["ci%d_s" % i] = MultiColorLabel(_(" N/A"))

			self["security%d_i" % i] = Label(_(" Security%d" % i))
			self["security%d_s" % i] = MultiColorLabel(_(" N/A"))

		self["usb0_i"] = Label(_(" Front USB"))
		self["usb0_s"] = MultiColorLabel(_(" N/A"))
		
		if not self.has_front_usb:
			self["usb0_i"].hide()
			self["usb0_s"].hide()
			
		self["usb1_i"] = Label(_(" Rear USB-1"))
		self["usb1_s"] = MultiColorLabel(_(" N/A"))
		self["usb2_i"] = Label(_(" Rear USB-2"))
		self["usb2_s"] = MultiColorLabel(_(" N/A"))

## will change rear 2 usb model for tmnanooe, optimussos1
#		if self.has_1_rear_usb:
#			self["usb1_i"].setText(_(" Rear USB"))
#			self["usb2_i"].hide()
#			self["usb2_s"].hide()

		for button in self.BUTTON_TEST:
			self[self.BUTTON_TEST[button]["button"]] = MultiColorLabel(_(self.BUTTON_TEST[button]["text"]))
			self[self.BUTTON_TEST[button]["button"]].hide()

	def layoutFinished(self):
		model = HardwareInfo().get_device_name() 
		if model == "optimussos1":
			self["info0_s"].setText(_(" OPTIMUSS OS1"))
		elif model == "optimussos2":
			self["info0_s"].setText(_(" OPTIMUSS OS2"))
		elif model == "optimussos1plus":
			self["info0_s"].setText(_(" OPTIMUSS OS1+"))
		elif model == "optimussos2plus":
			self["info0_s"].setText(_(" OPTIMUSS OS2+"))
		elif model == "force2solid":
			self["info0_s"].setText(_(" FORCE2"))
		elif model == "tmnanose":
			self["info0_s"].setText(_(" TM-NANO-SE"))
		elif model == "force2plus":
			self["info0_s"].setText(_(" FORCE2+"))
		elif model == "optimussosplus":
			self["info0_s"].setText(_(" OPTIMUSS OS+"))
		elif model == "tmnanosecombo":
			self["info0_s"].setText(_(" TM-NANO-SE Combo"))
		elif model == "tmnanosem2":
			self["info0_s"].setText(_(" TM-NANO-SE M2"))
		elif model == "force2eco":
			self["info0_s"].setText(_(" FORCE2 Eco"))
		elif model == "fusionhd":
			self["info0_s"].setText(_(" FUSION HD"))
		elif model == "force1plus":
			f = open("/etc/.brandtype", 'r')
			line = f.readline()
			if "technomate" in line:
				self["info0_s"].setText(_(" TM-NANO-3T COMBO"))
			elif "edision" in line:
				self["info0_s"].setText(_(" OPTIMUSS OS3+"))
			elif "swiss" in line:
				self["info0_s"].setText(_(" FORCE1+ SWISS"))
			elif "worldvision" in line:
				self["info0_s"].setText(_(" FORCE1+ WORLD VISION"))
			elif "iqon" in line:
				self["info0_s"].setText(_(" FORCE1+ IQON"))
			else:
				self["info0_s"].setText(_(" %s" % (about.getHardwareTypeString())))
			f.close()
		else:
			self["info0_s"].setText(_(" %s" % (about.getHardwareTypeString())))
		self["info1_s"].setText(_(" %s" % (self.TEST_PROG_VERSION)))
		self["mac_s"].setText(_(" %s" % self.getMacaddress()))
		self["micom_s"].setText(_(" %s" % self.getMicomVersion()))

		securityRes = self.checkSecurityChip()
		if securityRes == 0xf:
			for i in (0, 1):
				self["security%d_i" % i].hide()
				self["security%d_s" % i].hide()
		elif self.has_sc41cr:
			if securityRes:
				self["security0_s"].setText(_(" SC41CR - NOK"))
				self["security0_s"].setForegroundColorNum(1)
			else:
				self["security0_s"].setText(_(" SC41CR - OK"))
			self["security1_i"].hide()
			self["security1_s"].hide()
		elif self.has_sc50cr:
			if securityRes:
				self["security0_s"].setText(_(" SC50CR - NOK"))
				self["security0_s"].setForegroundColorNum(1)
			else:
				self["security0_s"].setText(_(" SC50CR - OK"))
			self["security1_i"].hide()
			self["security1_s"].hide()
		else:
			if securityRes>>1 & 1:
				self["security0_s"].setText(_(" CO164 - NOK"))
				self["security0_s"].setForegroundColorNum(1)
			else:
				self["security0_s"].setText(_(" CO164 - OK"))
			self["security1_i"].hide()
			self["security1_s"].hide()

		self.keyNumberGlobal(1)

		from enigma import eDVBVolumecontrol
		eDVBVolumecontrol.getInstance().setVolume(100, 100)

# ---------------------------------------------------------------------
#  menulist functions
# ---------------------------------------------------------------------

	def func(self, entry):
		self["menulist"].hide()
		if "ch1" in entry[1]:
			video_hw.setMode("Scart", "720p", "50Hz")
			config.av.colorformat.value = "cvbs"
			open("/proc/stb/video/aspect", "w").write("4:3")
			self.setTone("off")
			self.playService(entry[1])
		elif "ch2" in entry[1]:
			video_hw.setMode("YPbPr", "576i", "50Hz")
			config.av.colorformat.value = "yuv"
			open("/proc/stb/video/aspect", "w").write("4:3")
			self.setTone("off")
			self.playService(entry[1])
		elif "ch3" in entry[1]:
			video_hw.setMode("Scart", "576i", "50Hz")
			config.av.colorformat.value = "rgb"
			open("/proc/stb/video/aspect", "w").write("16:9")
			self.setTone("off")
			self.playService(entry[1])
		elif "ch4" in entry[1]:
			video_hw.setMode("Scart", "1080i", "50Hz")
			config.av.colorformat.value = "cvbs"
			open("/proc/stb/video/aspect", "w").write("16:9")
			self.setTone("off")
			self.playService(entry[1])
		elif "ch5" in entry[1]:
			video_hw.setMode("Scart", "576i", "50Hz")
			config.av.colorformat.value = "rgb"
			open("/proc/stb/video/aspect", "w").write("16:9")
			self.setTone("off")
			self.playService(entry[1])
		elif entry[1] == "tone":
			if "[ON]" in entry[0]:
				self.setTone("off")
			else:
				self.setTone("on")

			# TODO  - romove below channel change codes,
			# without channel change, tuner configuration does not change
			if self.service == "ch1":
				self.playService("ch2")
				self.playService("ch1")
			elif self.service == "ch2":
				self.playService("ch1")
				self.playService("ch2")
			elif self.service == "ch3":
				self.playService("ch4")
				self.playService("ch3")
			elif self.service == "ch4":
				self.playService("ch3")
				self.playService("ch4")
			elif self.service == "ch5": 
				self.playService("ch4")
				self.playService("ch5")

		elif entry[1] == "fan":
			if "[ON]" in entry[0]:
				self.setFan("off")
			else:
				self.setFan("on")
		elif entry[1] == "fp":
			self.fpTest()
		elif entry[1] == "ds":
			self.deepStandby()
		elif entry[1] == "exit":
			self.session.openWithCallback(self.quitConfirmed, MessageBox, _("Do you really want to quit?"), default = True)
		else:
			print "what", entry
		self["menulist"].show()

		# show vfd message
		index = 0
		for menu in self.MENU_LIST:
			if menu[1] == entry[1]:
				os.system("echo \"%s\" > /proc/stb/lcd/show_txt" % self.MENU_LIST[index][0])
				self.vfdTextWrite(self.MENU_LIST[index][0])
				break
			index += 1

	def changeMenuName(self, menuid, menutext):
		index = 0
		for menu in self.MENU_LIST:
			if menu[1] == menuid:
				self.MENU_LIST[index][0] = menutext
				break
			index += 1

		self.setMenuList(self.MENU_LIST)

# --------------------------------------------------------------------
# satellites.xml date version 22 Dec 2014 on /etc/.e2settings
#
# has 1 tunner.
# FRANCE24
# 1:0:1:8:1:FFFF:C00FA0:0:0:0:
# RTPi
# 1:0:1:1E:1:FFFF:C00FA0:0:0:0:
# DUBAI
# 1:0:1:1:1:FFFF:C08E4C:0:0:0:
# DUBAI SPORTS 3
# 1:0:1:2:1:FFFF:C08E4C:0:0:0:
#
# has 2 tunner or 3 tunner
# FRANCE24
# 1:0:1:8:1:FFFF:C90FA0:0:0:0:
# DUBAI
# 1:0:1:1:1:FFFF:C98E4C:0:0:0:
# DUBAI SPORTS 3
# 1:0:1:2:1:FFFF:C98E4C:0:0:0:
# RTPi
# 1:0:1:1E:1:FFFF:C90FA0:0:0:0:
#
# has 3 tunner : channel 5
# BBC NEWS 24
# 1:0:1:113F:1003:233A:EEEE0000:0:0:0:
#
#----------------------------------------------------------------------

	def playService(self, service=None):
		if service:
			self.service = service
		self.session.nav.stopService()
		
		if self.service == "ch1":
			self.session.nav.playService(eServiceReference("1:0:1:1E:1:FFFF:C00FA0:0:0:0:"))
#			print "[Service] : ch1->" + "1:0:1:1E:1:FFFF:C00FA0:0:0:0:"+"\n"
		elif self.service == "ch2":
			self.session.nav.playService(eServiceReference("1:0:1:1:1:FFFF:C08E4C:0:0:0:"))
#			print "[Service] : ch2->"+ "1:0:1:1:1:FFFF:C08E4C:0:0:0"+ "\n"
		elif self.service == "ch3":
			if len(nimmanager.nimList()) == 2:
				if self.has_7362_combo:
					self.session.nav.playService(eServiceReference("1:0:1:1E:1:FFFF:C00FA0:0:0:0:"))
				else:
					self.session.nav.playService(eServiceReference("1:0:1:8:1:FFFF:C00FA0:0:0:0:"))
#					print "[Service] : nim=2"+"ch3" + "1:0:1:8:1:FFFF:C80FA0:0:0:0"+ "\n"
			else:
				if len(nimmanager.nimList()) == 1:
					self.session.nav.playService(eServiceReference("1:0:1:8:1:FFFF:C00FA0:0:0:0:"))
#					print "[Service] : nim1" + "ch3"+"1:0:1:1E:1:FFFF:C00FA0:0:0:0"+"\n"
				if len(nimmanager.nimList()) == 3:
					self.session.nav.playService(eServiceReference("1:0:1:8:1:FFFF:C90FA0:0:0:0:"))
#					print "[Service] : nim3" + "ch3"+"1:0:1:8:1:FFFF:C80FA0:0:0:0"+ "\n"
		elif self.service == "ch4":
			if len(nimmanager.nimList()) == 2:
				if self.has_7362_combo:
					self.session.nav.playService(eServiceReference("1:0:1:2:1:FFFF:C08E4C:0:0:0:")) # DUBAI SPORTS
				else:
					self.session.nav.playService(eServiceReference("1:0:1:2:1:FFFF:C98E4C:0:0:0:"))
#					print "[Service] : nim2" + "ch4"+"1:0:1:2:1:FFFF:C88E4C:0:0:0"+"\n"
			else:
				if len(nimmanager.nimList()) == 1:
					self.session.nav.playService(eServiceReference("1:0:1:2:1:FFFF:C08E4C:0:0:0:")) # DUBAI SPORTS
#					print "[Service] : nim1" + "ch4"+"1:0:1:2:1:FFFF:C08E4C:0:0:0:"+"\n"
				if len(nimmanager.nimList()) == 3:
					self.session.nav.playService(eServiceReference("1:0:1:2:1:FFFF:C98E4C:0:0:0:"))
#					print "[Service] : nim3" +"ch4"+"1:0:1:2:1:FFFF:C88E4C:0:0:0"+ "\n"
		elif self.service == "ch5":
			#self.session.nav.playService(eServiceReference("1:0:1:1005:1:601:FFFF0000:0:0:0:"))			# Cable
			self.session.nav.playService(eServiceReference("1:0:1:113F:1004:233A:EEEE0000:0:0:0:")) 	# Terrestrial
			# self.session.nav.playService(eServiceReference("1:0:1:113F:1003:233A:EEEE0000:0:0:0:")) 	# Terrestrial
			
	def setTone(self, tone):
		config.Nims[0].advanced.sat[192].tonemode.value = tone
		if self.has_1_tuner:
			config.Nims[0].advanced.sat[201].tonemode.value = tone
		else:
			config.Nims[1].advanced.sat[201].tonemode.value = tone

		nimmanager.sec.update()

		if tone == "on":
			self.changeMenuName("tone", "22Khz	- [ON]/ OFF")
		else:
			self.changeMenuName("tone", "22Khz	-  ON /[OFF]")

# ---------------------------------------------------------------------
#  fp, CODE IS DIRTY
# ---------------------------------------------------------------------
	def frontButtonPass(self):
		return

	def frontButtonOk(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("ok"):
			return

		if pressed:
			self["button_ok"].show()
		else:
			self["button_ok"].hide()
		self.BUTTON_TEST["ok"]["pressed"] = pressed
		self.checkFpTestIsOk()

		os.system("echo VFD START > /proc/stb/lcd/show_txt")

	def frontButtonUp(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("up"):
			return

		if not self.has_nav_keys:
			return

		if pressed:
			self["button_up"].show()
		else:
			self["button_up"].hide()
		self.BUTTON_TEST["up"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonDown(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("down"):
			return

		if not self.has_nav_keys:
			return

		if not self.BUTTON_TEST.has_key("menu"):
			os.system("echo VFD START > /proc/stb/lcd/show_txt")

		if pressed:
			self["button_down"].show()
		else:
			self["button_down"].hide()
		self.BUTTON_TEST["down"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonLeft(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("left"):
			return

		if not self.has_nav_keys:
			return

		if pressed:
			self["button_left"].show()
		else:
			self["button_left"].hide()
		self.BUTTON_TEST["left"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonRight(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("right"):
			return

		if not self.has_nav_keys:
			return

		if pressed:
			self["button_right"].show()
		else:
			self["button_right"].hide()
		self.BUTTON_TEST["right"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonMenu(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("ok"):
			return

		if pressed:
			self["button_menu"].show()
		else:
			self["button_menu"].hide()
		self.BUTTON_TEST["menu"]["pressed"] = pressed
		self.checkFpTestIsOk()

		os.system("echo VFD START > /proc/stb/lcd/show_txt")

	def frontButtonExit(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("exit"):
			return

		if pressed:
			self["button_exit"].show()
		else:
			self["button_exit"].hide()
		self.BUTTON_TEST["exit"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonPower(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("power"):
			return

		if pressed:
			self["button_power"].show()
		else:
			self["button_power"].hide()
		self.BUTTON_TEST["power"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonChPlus(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("right"):
			return

		if pressed:
			self["button_right"].show()
		else:
			self["button_right"].hide()
		self.BUTTON_TEST["right"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonChMinus(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("left"):
			return

		if not self.BUTTON_TEST.has_key("menu"):
			os.system("echo VFD START > /proc/stb/lcd/show_txt")

		if pressed:
			self["button_left"].show()
		else:
			self["button_left"].hide()
		self.BUTTON_TEST["left"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonVolUp(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("up"):
			return

		if pressed:
			self["button_up"].show()
		else:
			self["button_up"].hide()
		self.BUTTON_TEST["up"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonVolDown(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("down"):
			return

		if pressed:
			self["button_down"].show()
		else:
			self["button_down"].hide()
		self.BUTTON_TEST["down"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def frontButtonInfo(self, pressed=True):
		if not self.fpTestMode:
			return

		if not self.BUTTON_TEST.has_key("info"):
			return

		if not self.has_key("button_info"):
			return

		if pressed:
			self["button_info"].show()
		else:
			self["button_info"].hide()
		self.BUTTON_TEST["info"]["pressed"] = pressed
		self.checkFpTestIsOk()

	def fpTestQuit(self):
		self.changeMenuName("fp", "FRONT PANEL")
		self.fpTestMode = False

		os.system("echo ^0^ > /proc/stb/lcd/show_txt")

	def checkFpTestIsOk(self):
			exit = True
			for button in self.BUTTON_TEST:
				if not self.BUTTON_TEST[button]["pressed"]:
					exit = False
					break
			if exit:
				for button in self.BUTTON_TEST:
					self[self.BUTTON_TEST[button]["button"]].setForegroundColorNum(1)
				self.changeMenuName("fp", "FRONT PANEL - OK")
				self.fpTestMode = False

				os.system("echo '^0^' > /proc/stb/lcd/show_txt")

	def vfdOn(self, on):
		fp = open('/dev/dbox/lcd0', 'w')
		fcntl.ioctl(fp.fileno(), 0x123321, on)

	def vfdTextWrite(self, text):
		return
		if self.has_vfd:
			if os.path.exists('/proc/stb/lcd/show_txt'):
				open('/proc/stb/lcd/show_txt', 'w').write(text)

	def fpTest(self):
		if self.fpTestMode:
			return

		self.fpTestMode = True
		self.changeMenuName("fp", " \"PRESS FRONT BUTTONS(RED TO QUIT)\"")

		os.system("echo VFD START > /proc/stb/lcd/show_txt")

		for button in self.BUTTON_TEST:
			self.BUTTON_TEST[button]["func"](False)
			self[self.BUTTON_TEST[button]["button"]].setForegroundColorNum(0)

# ---------------------------------------------------------------------
# fan 
# ---------------------------------------------------------------------
	def setFan(self, power):
		if power == "on":
			self.changeMenuName("fan", "FAN	- [ON]/ OFF")
			fancontrol.setPWM(0, 255)
		else:
			self.changeMenuName("fan", "FAN	-  ON /[OFF]")
			fancontrol.setPWM(0, 0)

# ---------------------------------------------------------------------
# deep standby 
# ---------------------------------------------------------------------
	def deepStandby(self):
		self.session.openWithCallback(self.deepStandbyConfirmed, MessageBox, _("Do you really want to go to Deep Standby?"), default = True)

	def deepStandbyConfirmed(self, answer):
		if answer:
			self.quit(1)

# ---------------------------------------------------------------------
#  lan check
# ---------------------------------------------------------------------
	def getLinkState(self):
		try:
			iNetwork.getLinkState(self.iface, self.dataAvail)
		except:
			pass

	def dataAvail(self, data):
		# sidabary-lan-test
		###lan debug print "-----------------------------------------------"
		###lan debug print data
		###lan debug print "-----------------------------------------------"
		
		self.LinkState = None

		# sidabary-lan-test
		self.LinkSpeed = None
		
		for line in data.splitlines():
			line = line.strip()
			if 'Link detected:' in line:
				if "yes" in line:
					self.LinkState = True
				else:
					self.LinkState = False

			#sidabary-lan-test						
			if 'Speed:' in line:
				if line.find("1000M",6) >= 0:
					self.LinkSpeed = "(1G-bits)"
				else:
					if line.find("100M",6) >= 0:
						self.LinkSpeed = "(100M-bits)"						
					else:
						self.LinkSpeed = "(error)"
						
		if self.LinkState == True:
			#iNetwork.checkNetworkState(self.checkNetworkCB) ## old state
			self.checkNetworkCB()
		else:
			self["lan_s"].setText(_(" N/A"))
			self["lan_s"].setForegroundColorNum(0)
			self.networkMonitor.start(1000, True)

	# def checkNetworkCB(self,data): ## old state
	def checkNetworkCB(self):
		try:
			# sidabary-lan-test
			###lan debug print "**************************************************"
			###lan debug print self.LinkSpeed
			###lan debug print self.LinkSpeed
			###lan debug print self.LinkSpeed
			###lan debug print "**************************************************"			
			## new data = 1 insert
			data = 1
			if iNetwork.getAdapterAttribute(self.iface, "up") is True:
				if self.LinkState is True:

					#  sidabary-lan-test
					#  if data <= 2:
					# if data <=3:  ## old state
					if data == 1:
						ip = NoSave(ConfigIP(default=iNetwork.getAdapterAttribute(self.iface, "ip")) or [0,0,0,0]).getText()
						if ip == "0.0.0.0":
							self.networkMonitor.stop()
							self.restartLan()
							self["lan_s"].setText(_(" Getting..."))
							self["lan_s"].setForegroundColorNum(0)
							return
							
						# sidabary-lan-test
						self["lan_s"].setText(_(" %s ") % (ip + "    " + self.LinkSpeed))
						self["lan_s"].setForegroundColorNum(1)
					else:
						self["lan_s"].setText(_(" N/A"))
						self["lan_s"].setForegroundColorNum(0)
				else:
					self["lan_s"].setText(_(" N/A"))
					self["lan_s"].setForegroundColorNum(0)
			else:
				self["lan_s"].setText(_(" N/A"))
				self["lan_s"].setForegroundColorNum(0)
			self.networkMonitor.start(1000, True)
		except:
			pass

	def restartLan(self):
		iNetwork.restartNetwork(self.restartLanDataAvail)
			
	def restartLanDataAvail(self, data):
		if data is True:
			iNetwork.getInterfaces(self.getInterfacesDataAvail)

	def getInterfacesDataAvail(self, data):
		if data is True:
			self.networkMonitor.start(1000, True)

# ---------------------------------------------------------------------
#  smartcard check
# ---------------------------------------------------------------------
	def getSCInfo(self, slot = 0):
		card = "N/A"
		device = open("/dev/sci%d" % slot, "rw")
		try:
			fcntl.ioctl(device.fileno(), 0x80047301)
			atr = device.read()
			for atrHead in self.CARD_LIST.keys():
				if atr.startswith(atrHead):
					card = self.CARD_LIST[atrHead]
		except:
			card = "Unknown"
		return card

	def checkSCSlot(self, slot = 0):
		inserted = array.array('h', [0])
		try:
			device = open("/dev/sci%d" % slot, "rw")
		except:
			os.system("/etc/init.d/softcam stop; /etc/init.d/cardserver stop")
			return False
		fcntl.ioctl(device.fileno(), 0x80047308, inserted, 1)
		device.close()
		return inserted[0]

	def getSCState(self):
		for slot in (0, 1):
			if os.path.exists("/dev/sci%d" % slot):
				if self.checkSCSlot():
					if not self.smartcardInserted[slot]:
						scInfo = self.getSCInfo(slot)
						self["sc%d_s" % slot].setText(_(" %s" % scInfo))
						if scInfo != "Unknown":
							self["sc%d_s" % slot].setForegroundColorNum(1)
						else:
							self["sc%d_s" % slot].setForegroundColorNum(0)
					self.smartcardInserted[slot] = True
				else:
					## if self.smartcardInserted[slot]:
					self["sc%d_s" % slot].setText(_(" N/A"))
					self["sc%d_s" % slot].setForegroundColorNum(0)
					self.smartcardInserted[slot] = False
			else:
				self["sc%d_i" % slot].hide()
				self["sc%d_s" % slot].hide()

# ---------------------------------------------------------------------
#  ci check
# ---------------------------------------------------------------------
	def getCIState(self):
		for slot in (0, 1):
			if os.path.exists("/dev/ci%d" % slot):
				state = eDVBCI_UI.getInstance().getState(slot)
				if state == 1:
					self["ci%d_s" % slot].setText(_(" Getting..."))
					self["ci%d_s" % slot].setForegroundColorNum(0)
				elif state == 2:		#module ready
					self["ci%d_s" % slot].setText(_(" %s" % eDVBCI_UI.getInstance().getAppName(slot)))
					self["ci%d_s" % slot].setForegroundColorNum(1)
					eDVBCI_UI.getInstance().stopMMI(slot)
				else:
					self["ci%d_s" % slot].setText(_(" N/A"))
					self["ci%d_s" % slot].setForegroundColorNum(0)
			else:
				self["ci%d_i" % slot].hide()
				self["ci%d_s" % slot].hide()

# ---------------------------------------------------------------------
#  usb, sata check
# ---------------------------------------------------------------------
	def getStorageState(self):
		storageFound = {}
		try:
			for hd in harddiskmanager.HDDList():
				if hd[1].model().split("(")[0] == "ATA":
					storageFound["sata_s"] = hd[1].model()
				else:
					for realpath in self.USBDB[HardwareInfo().get_device_name()]:
						if realpath in os.path.realpath('/sys/block/' + hd[1].device[:3] + '/device')[4:]:
							storageFound["usb%d_s" % self.USBDB[HardwareInfo().get_device_name()][realpath]] = hd[1].model()
		except:
			return

		for storage in ("sata_s", "usb0_s", "usb1_s", "usb2_s"):
			if storageFound.has_key(storage):
				self[storage].setText(_(" %s" % storageFound[storage]))
				self[storage].setForegroundColorNum(1)
			else:
				self[storage].setText(_(" N/A"))
				self[storage].setForegroundColorNum(0)

# ---------------------------------------------------------------------
#  mac address check
# ---------------------------------------------------------------------
	def getMacaddress(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', self.iface[:15]))
		return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]

# ---------------------------------------------------------------------
#  micom version check
# ---------------------------------------------------------------------
	def getMicomVersion(self):
		if HardwareInfo().has_micom():
			return about.getMicomVersionString()
		else:
			return "N/A"

# ---------------------------------------------------------------------
#  security chip check
# ---------------------------------------------------------------------
	def checkSecurityChip(self):
		fp = open('/dev/dbox/fp0', 'w')
		try:
			return fcntl.ioctl(fp.fileno(), 0x417)
		except:
			return 0xf

# ---------------------------------------------------------------------
# fan status check
# ---------------------------------------------------------------------
	def initFanSensors(self):
		templist = sensors.getSensorsList(sensors.TYPE_TEMPERATURE)
		tempcount = len(templist)
		fanlist = sensors.getSensorsList(sensors.TYPE_FAN_RPM)
		fancount = len(fanlist)
		
		for count in range(8):
			if count < tempcount:
				id = templist[count]
				self["SensorTempText%d" % count] = StaticText(sensors.getSensorName(id))		
				self["SensorTemp%d" % count] = SensorSource(sensorid = id)
			else:
				self["SensorTempText%d" % count] = StaticText("")
				self["SensorTemp%d" % count] = SensorSource()
				
			if count < fancount:
				id = fanlist[count]
				self["SensorFanText%d" % count] = StaticText(sensors.getSensorName(id))		
				self["SensorFan%d" % count] = SensorSource(sensorid = id)
			else:
				self["SensorFanText%d" % count] = StaticText("")
				self["SensorFan%d" % count] = SensorSource()

