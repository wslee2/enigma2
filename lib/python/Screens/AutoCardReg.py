from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Sources.List import List
from Components.config import getConfigListEntry, config, ConfigBoolean, ConfigNothing, ConfigSlider
from Components.ConfigList import ConfigList
from Components.Label import Label
from Components.config import config, ConfigElement, ConfigSubsection, ConfigSelection, ConfigSubList, getConfigListEntry, KEY_LEFT, KEY_RIGHT, KEY_OK
from enigma import eTimer
import os
from Screens.MessageBox import MessageBox
from enigma import AutoPwd

from Plugins.PLi.SoftcamSetup.camcontrol import CamControl

class AutoCardReg(Screen):
	skin = """
		<screen name="AutoCardReg" position="center,center" size="560,230" title="SETUP LOADER">
			<widget name="entries" position="5,10" size="550,140" />
			<ePixmap name="green" position="280,190" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
			<ePixmap name="blue" position="420,190" zPosition="1" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
			<widget name="key_green" position="280,190" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
			<widget name="key_blue" position="420,190" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
			<widget name="static_ip" position="10,160" zPosition="2" size="530,40" valign="center" halign="left" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)

		print "# AutoCardReg"
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions","CiSelectionActions"],
		{
			"left": self.keyLeft,
			"right": self.keyRight,
			"ok": self.ok,
			"cancel": self.close,
			"green": self.monitor,
			"blue": self.save,
		}, -1)

		self["key_blue"] = Label(_("Save"))
		self["key_green"] = Label(_("Monitor"))
		self["static_ip"] = Label(_("Static IP : Please wait..."))

		self.list = [ ]
		self.menuList = ConfigList(self.list)
		self.menuList.list = self.list
		self.menuList.l.setList(self.list)
		self["entries"] = self.menuList

		self.static_ip=None
		self.StaticIPTimer = eTimer()
		self.StaticIPTimer.callback.append(self.iptimeout)

		self.gateway="192.168.1.1"
		self.current_cardnum ="C - 01"
		self.init()
		self.reload_list()
		self.StaticIPTimer.start(500, True)	
		self.hide()

	def monitor(self):
		print "# monitor"
		self.session.open(MessageBox, _("Please wait....Opening Port for Monitoring..."), type = MessageBox.TYPE_INFO, timeout = 25, default = False)
		self.getDefaultGateway()
		self.changeIP()

		if self.type.find('CCCAM') != -1:
			cmd="/etc/upnpc -d %d TCP; /etc/upnpc -a %s 23 %d TCP" % (2323+self.port-45000, self.ip, 2323+self.port-45000)
		else:
			cmd="/etc/upnpc -d %d TCP; /etc/upnpc -a %s 23 %d TCP" % (2323+self.port-44000, self.ip, 2323+self.port-45000)

		print "# cmd => ", cmd
		os.system(cmd)

	def iptimeout(self):
		print "## iptimeout "
		if self.type != "CCCAM":
			self.session.open(MessageBox, _("Sorry, only CCcam support"), type = MessageBox.TYPE_ERROR, timeout = 5, default = False)
			self.close()
			return
		else:
			self.show()
	
		if os.path.isfile("/tmp/extip"):
			fp = file('/tmp/extip', 'r')
			static_ip = fp.read()
			fp.close()
			if static_ip=="":
				print "## ", self.timeout_count
				if self.timeout_count == 3 :
					os.system("wget -O /tmp/extip -T 4 -t 1 http://ilove.hobby-site.com/un/iprequest.php")
					self.timeout_count=0
				else :
					self.timeout_count=self.timeout_count+1
			else:
				print "OK : ",static_ip
				self.StaticIPTimer.stop()
				self["static_ip"].setText(_("Static IP : ")+static_ip)
				self.static_ip=static_ip
				return
				#self["description"].setText(_("Edit the network configuration of your Linuxbox.\n" ) + self.oktext + _("\n\n Static IP :") + static_ip)
		else:
			self.timeout_count=3
			os.system("wget -O /tmp/extip -T 2 -t 1 http://ilove.hobby-site.com/un/iprequest.php")

		self.StaticIPTimer.stop()
		self.StaticIPTimer.start(3000, True)	

	def reload_list(self):
		self.list = [ ]

		#readertype = ["Local", "Smargo"]
		readertype = ["Local"]
		self.readertype = ConfigSelection(choices = readertype)
		self.readertype.value = "Local"
		self.list.append(getConfigListEntry(_("Reader Type"), self.readertype))

		emu = [self.type]
		self.emu = ConfigSelection(choices = emu)
		self.emu.value = self.type
		self.list.append(getConfigListEntry(_("EMU"), self.emu))

		cid = ["C - 01", "C - 02", "C - 03", "C - 04", "C - 05", "C - 06", "C - 07", "C - 08", "C - 09", "C - 10"]
		self.cid = ConfigSelection(choices = cid)
		self.cid.value = self.current_cardnum
		self.list.append(getConfigListEntry(_("C-ID"), self.cid))

		self.menuList.l.setList(self.list)

	def init(self):
		if os.path.isfile("/tmp/extip"):
			os.system("rm -f /tmp/extip")

		self.softcam = CamControl('softcam')
		print "# selected ", self.softcam.current()

		self.link_softcam = os.readlink('/etc/init.d/softcam')
		self.link_cardserver = os.readlink('/etc/init.d/cardserver')
		if self.link_softcam.find('mgcamd') != -1:
			self.readNewcsPort()
			if self.link_cardserver.find('newcs') != -1:
				self.type = "NEWCAMD"
				self.setTitle("SETUP LOADER - NEWCAMD");
			else: 
				self.type = "None"
				self.setTitle("SETUP LOADER - None");
		elif self.link_softcam.find('CCcam') != -1:
			self.readCCcamPort()
			self.setTitle("SETUP LOADER - CCCAM");
			if self.link_cardserver.find('oscam') != -1:
				self.type = "CCCAM+OSCAM"
			elif self.link_cardserver.find('newcs') != -1:
				self.type = "CCCAM+NEWCS"
			else:
				self.type = "CCCAM"
		else:
			self.type = "None"
			self.setTitle("SETUP LOADER - None");
		
	def readCCcamPort(self):
		print "#readCCcamPort"
		f=open('/etc/.CCcam.cfg', 'r')
		lines = f.readlines()
		f.close()
		self.current_cardnum ="C - 01"
		for line in lines:
			if line.find('SERVER LISTEN PORT :') != -1:
				if line[0] != '#':
					if line.find('45000') != -1:
						self.current_cardnum = 'C - 01'
					elif line.find('45001') != -1:
						self.current_cardnum = 'C - 02'
					elif line.find('45002') != -1:
						self.current_cardnum = 'C - 03'
					elif line.find('45003') != -1:
						self.current_cardnum = 'C - 04'
					elif line.find('45004') != -1:
						self.current_cardnum = 'C - 05'
					elif line.find('45005') != -1:
						self.current_cardnum = 'C - 06'
					elif line.find('45006') != -1:
						self.current_cardnum = 'C - 07'
					elif line.find('45007') != -1:
						self.current_cardnum = 'C - 08'
					elif line.find('45008') != -1:
						self.current_cardnum = 'C - 09'
					elif line.find('45009') != -1:
						self.current_cardnum = 'C - 10'
					else:
						self.current_cardnum = 'C - 01'

	def readNewcsPort(self):
		print "#readNewcsPort"
		f=open('/etc/tuxbox/config/newcs.xml', 'r')
		lines = f.readlines()
		f.close()
		self.current_cardnum ="C - 01"
		for line in lines:
			if line.find('<newcamd_port>') != -1:
				if line[0] != '#':
					if line.find('44000') != -1:
						self.current_cardnum = 'C - 01'
					elif line.find('44001') != -1:
						self.current_cardnum = 'C - 02'
					elif line.find('44002') != -1:
						self.current_cardnum = 'C - 03'
					elif line.find('44003') != -1:
						self.current_cardnum = 'C - 04'
					elif line.find('44004') != -1:
						self.current_cardnum = 'C - 05'
					elif line.find('44005') != -1:
						self.current_cardnum = 'C - 06'
					elif line.find('44006') != -1:
						self.current_cardnum = 'C - 07'
					elif line.find('44007') != -1:
						self.current_cardnum = 'C - 08'
					elif line.find('44008') != -1:
						self.current_cardnum = 'C - 09'
					elif line.find('44009') != -1:
						self.current_cardnum = 'C - 10'
					else:
						self.current_cardnum = 'C - 01'
	
	def getNameserver(self):
		fp_read = file('/etc/resolv.conf', 'r')
		line = fp_read.read()
		fp_read.close()
		line = line.split()
		#TM800@/]# cat /etc/resolv.conf
		#nameserver 192.168.1.1
		self.nameserver = line[1]
		print "#nameserver =", self.nameserver

	def getDefaultGateway(self):
		os.system('route -n | grep eth0 > /tmp/.route')
		#TM800@/]# cat /tmp/.route
		#192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0
		#224.0.0.0       0.0.0.0         240.0.0.0       U     0      0        0 eth0
		#0.0.0.0         192.168.1.1     0.0.0.0         UG    0      0        0 eth0

		#192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0
		#0.0.0.0         192.168.1.1     0.0.0.0         UG    0      0        0 eth0

		fp_read = file('/tmp/.route', 'r')
		lines = fp_read.readlines()
		fp_read.close()
		for line in lines:
			line = line.split()
			if line[0] == "0.0.0.0":
				self.gateway=line[1]
		print "#gateway = ", self.gateway

	def writeNetworkConfig(self):
		self.configuredInterfaces = []
		fp_read = file('/etc/network/interfaces', 'r')
		lines = fp_read.readlines()
		fp_read.close()

		fp_write = file('/etc/network/interfaces', 'w')
		for line in lines:
			if line.find('iface eth0 inet') != -1:
				if line.find('iface eth0 inet dhcp') != -1:
					fp_write.write('iface eth0 inet static\n')
					fp_write.write("	address %s\n" % self.ip)
					fp_write.write("	netmask 255.255.255.0\n")
					fp_write.write("	gateway %s\n" % self.gateway)
					break
				else:
					fp_write.write('iface eth0 inet static\n')
			elif line.find('address') != -1:
				fp_write.write("	address %s\n" % self.ip )
			elif line.find('gateway') != -1:
				fp_write.write("	gateway %s\n" % self.gateway)
			else:
				fp_write.write(line)

		fp_write.close()
		os.system("/etc/init.d/networking restart")

	def save(self):
		print "#save"
		print self.readertype.value
		print self.cid.value

		if os.path.isfile("/etc/default_gw"):
			fp = file('/etc/default_gw', 'r')
			result = fp.read()
			fp.close()
			print "==> ", result
			if result.find('eth0') == -1 :
				self.session.open(MessageBox, _("Sorry, support only Integrated Ethernet(eth0)"), type = MessageBox.TYPE_WARNING, timeout = 5, default = False)
				return

		if self.static_ip == None:
			print "# not internet "
			self.session.open(MessageBox, _("Static ip is empty"), type = MessageBox.TYPE_WARNING, timeout = 5, default = False)
			return

		self.getDefaultGateway()
		self.getNameserver()
		self.changeIP()

		if self.type == "CCCAM" : #or self.type == "CCCAM+OSCAM" or self.type == "CCCAM+NEWCS":
			print "# selected cccam port ", self.cid.value 
			self.MakeCCcam()
		#elif self.type == "NEWCAMD" :
		#	print "# selected newcamd port ", self.cid.value 
		#	self.MakeMgcamd()
		else:
			print "# error", self.cid.value
			self.session.open(MessageBox, _("Sorry, it support only CCcam in EMU"), type = MessageBox.TYPE_WARNING, timeout = 5, default = False)
			return

		self.StaticIPTimer.stop()
		self.session.open(MessageBox, _("Wait : Restarting LAN Connection"), type = MessageBox.TYPE_INFO, timeout = 25)
		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.doStop)
		self.activityTimer.start(100, False)

	def doStop(self):
		self.activityTimer.stop()

		print "######### stop #############"
		self.softcam.command('stop')
		self.oldref = self.session.nav.getCurrentlyPlayingServiceReference()
		self.session.nav.stopService()
		os.system("rm -f /tmp/ecm*.info")

		from enigma import AutoPwd
		AutoPwd.getInstance().download_info()

		self.writeNetworkConfig()
		self.upnpc()

		print "# AutoPwd"
		AutoPwd.getInstance().Reloading()

		self.activityTimer = eTimer()
		self.activityTimer.timeout.get().append(self.doStart)
		self.activityTimer.start(1000, False)

	def doStart(self):
		self.activityTimer.stop()
		del self.activityTimer 

		self.softcam.command('start')

		#import time
		#time.sleep(4)
		print "########### play ##################"
		self.session.nav.playService(self.oldref)
		del self.oldref
		self.close()

	def MakeCCcam(self):
		print "# MakeCCcam ", self.cid.value
		fr=open('/etc/.CCcam.cfg', 'r')
		lines = fr.readlines()
		fr.close()

		fw=open('/etc/.CCcam.cfg', 'w')

		fw.write("SERVER LISTEN PORT : %d\n" % self.port)	
		print "# server listen port ", self.port

		if self.type.find('CCCAM+OSCAM') != -1 :
			fw.write("F: server server 1 0 0\n")	
			for line in lines:
				if line.find("dummy dummy") != -1:
					fw.write("N: 127.0.0.1 %d dummy dummy 01 02 03 04 05 06 07 08 09 10 11 12 13 14\n", self.port-1000)
					continue
				if line.find("F: server server") != -1:
					continue
				elif line.find("SERVER LISTEN PORT") != -1:
					continue
				else:
					fw.write(line)
		elif self.type.find('CCCAM+NEWCS') != -1:
			fw.write("F: server server 1 0 0\n")	
		else: # only CCcam
			fw.write("F: server server 0 0 0\n")	
			for line in lines:
				if line.find("F: server server") != -1:
					continue
				elif line.find("SERVER LISTEN PORT") != -1:
					continue
				else:
					fw.write(line)
		fw.close()

	def MakeMgcamd(self):
		print "# MakeMgcamd ", self.cid.value

	def changeIP(self):
		if self.cid.value == "C - 01":
			port = 0
		elif self.cid.value == "C - 02":
			port = 1
		elif self.cid.value == "C - 03":
			port = 2
		elif self.cid.value == "C - 04":
			port = 3
		elif self.cid.value == "C - 05":
			port = 4
		elif self.cid.value == "C - 06":
			port = 5
		elif self.cid.value == "C - 07":
			port = 6
		elif self.cid.value == "C - 08":
			port = 7
		elif self.cid.value == "C - 09":
			port = 8
		elif self.cid.value == "C - 10":
			port = 9

		gat=self.gateway
		gat=gat.split('.')
		if self.type.find('CCCAM') != -1:
			self.port=45000+port
			self.ip = "%s.%s.%s.%d" % (gat[0],gat[1],gat[2], 230+port)
			print "#detected CCcam ->", self.type
		else:
			self.port=44000+port
			self.ip = "%s.%s.%s.%d" % (gat[0],gat[1],gat[2], 220+port)
			print "#detected Mgcamd ->", self.type
		
		print "# port =>", self.port 
		print "# ip =>", self.ip 

	def upnpc(self):
		print "# upnpc "

		print "# ext ip : ", self.static_ip
		print "# change ip : ", self.ip

		cmd="wget http://ilove.hobby-site.com/sr2/port_check.php?ip=%s.%d  -O /tmp/.ucheck" % (self.static_ip, self.port)
		print "# cmd => ", cmd
		os.system(cmd)
		fp = file('/tmp/.ucheck', 'r')
		quest = fp.read()
		fp.close()

		if quest == "N":
			print "# upnp not open"
			cmd="/etc/upnpc -d %d TCP; (/etc/upnpc -a %s %d %d TCP | tail -n -1) > /tmp/.upnp 2> /tmp/.upnp_error" % (self.port, self.ip, self.port, self.port)
			print "# cmd => ", cmd
			os.system(cmd)

			fp=file('/tmp/.upnp', 'r')
			msg_upnp=fp.read()
			fp.close()

			fp=file('/tmp/.upnp_error', 'r')
			msg_upnp_error=fp.read()
			fp.close()
			os.system("rm /tmp/.upnp; rm /tmp/.upnp_error")
			
			if msg_upnp_error.find('No IGD UPnP"') != -1:
				self.session.open(MessageBox, _("Check your router : No UPnP Device found on the network"), type = MessageBox.TYPE_ERROR, timeout = 5, default = False)
		else:
			print "# upnp open"


	def keyLeft(self):
		print "# keyleft"
		self["entries"].handleKey(KEY_LEFT)

	def keyRight(self):
		print "# keyright"
		self["entries"].handleKey(KEY_RIGHT)

	def ok(self):
		print "# ok"
		self["entries"].handleKey(KEY_OK)

	def changedEntry(self):
		for x in self.onChangedEntry:
			x()

	def changed(self):
		print "# changed"
