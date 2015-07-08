#include <netinet/in.h>
#include <sys/ioctl.h>
#include <linux/if.h>

#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "sr.h"

#define PROC_HWMODEL        "/proc/stb/info/hwmodel"


/********************************************************************************************/
/* class AutoPasswd																		*/
/********************************************************************************************/
AutoPasswd *AutoPasswd::instance;

AutoPasswd::AutoPasswd()
{
	instance = this;
}

AutoPasswd::~AutoPasswd()
{
	instance = 0;
}

AutoPasswd* AutoPasswd::getInstance()
{ 
	return instance; 
}

char* AutoPasswd::getMacAddr(const char *device)
{
	int sock, ret = 0;
	struct ifreq ifr;

	sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if(sock < 0)
		ret = -1;

	strncpy(ifr.ifr_name, device, IFNAMSIZ);
	ifr.ifr_addr.sa_family = AF_INET;

	ret = ioctl(sock, SIOCGIFHWADDR, &ifr);
	close(sock);

	if(ret < 0)
		sprintf(m_mac, "ffffffffffff");
	else
	{
		sprintf(m_mac,"%02x%02x%02x%02x%02x%02x",
				ifr.ifr_hwaddr.sa_data[0]&0xff,
				ifr.ifr_hwaddr.sa_data[1]&0xff,
				ifr.ifr_hwaddr.sa_data[2]&0xff,
				ifr.ifr_hwaddr.sa_data[3]&0xff,
				ifr.ifr_hwaddr.sa_data[4]&0xff,
				ifr.ifr_hwaddr.sa_data[5]&0xff);
	}

	return m_mac;
}

int AutoPasswd::checkMacAddr()
{
	int i;

	if(!m_mac)
		return -1;

	if(strstr(m_mac, "001752") != NULL || strstr(m_mac, "0cc6ac") != NULL)
	{
		/* mac address form should be xxxxxxXXXXXX ex> 0cc6ac0008E99 */
		for(i = 6; m_mac[i] != 0; i++)
		{
			if(m_mac[i] >= 'a' && m_mac[i] <= 'z')
				m_mac[i] = m_mac[i] - 32;
		}

		genPasswd();

		return 0;
	}
	else
		return -3;
}

int AutoPasswd::checkPasswd(const char *oldPasswd, const char *passwdFile)
{
	if(!checkMacAddr())
	{
		if(access(passwdFile, F_OK) == 0)
		{
			char passwd[255], buf[255], *check, salt[12];

			FILE *in = fopen(passwdFile, "r");
			fgets(buf, 255, in);
			fclose(in);

			*strstr(buf, ":0:0:root:") = '\0';
			strcpy(passwd, &buf[5]);

			salt[0] = passwd[0];
			salt[1] = passwd[1];
			salt[2] = passwd[2];
			salt[3] = '\0';

			check = crypt(oldPasswd, salt);

			if(!strcmp(check, passwd))
				return 0;
			else
				return 1;
		}
		return -1;
	}
	else
		return -1;
}

void AutoPasswd::setDate(const char *date)
{
	strcpy(m_date, date);
}

int AutoPasswd::getPasswdStr(char *passwd)
{
	char buf[32];
	int defaultPasswd = 1;
	int day = 0, month = 0, year = 0;
	
	if(m_date && strlen(m_date) == 11)	// m_date form should be "Dec 12 2012"(__DATE__)
	{
		const char monthNames[] = "JanFebMarAprMayJunJulAugSepOctNovDec";

		char sMonth[5] = {0,};

		sscanf(m_date, "%s %d %d", sMonth, &day, &year);
		month = (strstr(monthNames, sMonth) - monthNames) / 3 + 1;
		year = year % 100;

		defaultPasswd = 0;
	} 

	if(defaultPasswd && access("/proc/stb/info/buildate", F_OK) == 0)
	{
		FILE *in = fopen("/proc/stb/info/buildate", "r");
		if(in != NULL)
		{
			if(fgets(buf, 255, in) != NULL)
			{
				sscanf(buf, "%d/%d/%d", &day, &month, &year);
				defaultPasswd = 0;
			}

			fclose(in);
		}
	}

	if(defaultPasswd)
		sprintf(passwd, "!@#\\$qwerasdf");
	else
		sprintf(passwd, "!@#\\$qwer%02d%02d%02d", day, month, year);

	return 0;
}

void AutoPasswd::changePasswd(void)
{
	char buf[255];
	char passwd[255];

	/* backup passwd file */
	if(access("/etc/.passwd", F_OK) != 0)
		system("cp /etc/passwd /etc/.passwd");

	getPasswdStr(passwd);
	sprintf(buf, "(echo \"%s\";sleep 1;echo \"%s\";) | passwd", passwd, passwd);
	system(buf);
}

void AutoPasswd::restorePasswd(void)
{
	if(access("/etc/.passwd", F_OK) == 0)
		system("mv /etc/.passwd /etc/passwd");
	else
		/* shoud reset or remain the passwd when not exist backup passwd file? */
		system("(echo \"\"; sleep 1; echo \"\";) | passwd");
}

void AutoPasswd::genPasswd()
{
	char tmp;
	char key[55];
	char salt[] = "t8";
	int i;

	for(i=0; i<12; i++)
		key[i] = m_mac[11-i];
	key[i] = '\0';

	tmp = key[0]; 
	key[0] = key[7]; 
	key[7] = tmp;

	salt[0]= salt[1] + 3;       
	salt[1]= key[3] + 6;

	strcpy(m_passwd, crypt(key, salt));
}


/********************************************************************************************/
/* class SR																						*/
/********************************************************************************************/
SR *SR::instance;

SR::SR()
{
	char buf[32];
	instance = this;

	m_disable_cs = 1;

	m_model = MODEL_UNKNOWN;

	if(access(PROC_HWMODEL, F_OK) == 0) 
	{
		FILE *in = fopen(PROC_HWMODEL, "r");
		fgets(buf,32,in);
		fclose(in);

		if(strstr(buf, "tmtwin") != NULL)
			m_model = MODEL_TMTWIN;
		else if(strstr(buf, "tm2t") != NULL)
			m_model = MODEL_TM2T;
		else if(strstr(buf, "tmsingle") != NULL)
			m_model = MODEL_TMSINGLE;
		else if(strstr(buf, "tmnano") != NULL)
			m_model = MODEL_TMNANO;
		else if(strstr(buf, "ios100hd") != NULL)
			m_model = MODEL_IOS100HD;
		else if(strstr(buf, "ios200hd") != NULL)
			m_model = MODEL_IOS200HD;
		else if(strstr(buf, "ios300hd") != NULL)
			m_model = MODEL_IOS300HD;
		else if(strstr(buf, "tmnano2super") != NULL)
			m_model = MODEL_TMNANO2SUPER;
	    else if(strstr(buf, "force1") != NULL)
		    m_model = MODEL_FORCE1;
		else if(strstr(buf, "force1plus") != NULL)
			m_model = MODEL_FORCE1PLUS;	
		else if(strstr(buf, "tmnano2t") != NULL)
			m_model = MODEL_TMNANO2T;
	}

	if(m_model != MODEL_UNKNOWN)
	{
		printf("detected model %s\n", buf);
		getMacAddr();
	}
	else
		printf("detected unknown model\n");
}

SR::~SR()
{
	instance = 0;
}

SR *SR::getInstance()
{
	return instance;
}

char* SR::genPasswdLCS()
{
	/*
	$id=$_SESSION['login_id']."_"."001752".$_POST['id'];
	$pass=$_POST[id]."a700fZ9";
	$hash = crypt($pass, "qw");
	*/

	char passwd[50];
	strcpy(passwd, &m_mac[6]);
	strcat(passwd, "a700fZ9");

	for(int i = 0; i < 6; i++)
	{
		if(passwd[i] >= 'a' && passwd[i] <= 'z')
			passwd[i] = passwd[i] - ('a' - 'A');
	}

	return crypt(passwd, "qw");
}

void SR::genCCcamConfig()
{
	if (m_model != MODEL_UNKNOWN)
	{
		if(access("/var/etc/.CCcam.cfg", F_OK) != 0)
			system("cat /var/etc/CCcam.cfg > /etc/.CCcam.cfg");

		system("cat /var/etc/.CCcam.cfg > /etc/CCcam.cfg");

		if(access("/var/etc/.serverinfo_cccam", F_OK) == 0)
			system("cat /var/etc/.serverinfo_cccam >> /etc/CCcam.cfg");

		system("echo \"DISABLE EMM : no\" >> /etc/CCcam.cfg");
		system("echo \"ALLOW TELNETINFO: no\" >> /etc/CCcam.cfg");
		system("echo \"ALLOW WEBINFO: no\" >> /etc/CCcam.cfg");
	}
}

void SR::genMgcamdConfig()
{
	if(m_model != MODEL_UNKNOWN) 
	{
		if(access("/var/keys/.newcamd.list", F_OK) != 0) 
			system("cat /var/keys/newcamd.list > /var/keys/.newcamd.list");

		system("cat /var/keys/.newcamd.list > /var/keys/newcamd.list");

		if(access("/var/keys/.serverinfo_mgcamd", F_OK) == 0)
			system("cat /var/keys/.serverinfo_mgcamd >> /var/keys/newcamd.list"); 
	}
}

int SR::checkSR()
{
	if(access("/etc/.4dsmode", F_OK) != 0)
		return -1;

	/* not work
	char passwd[255];
	getPasswdStr(passwd);
	if(checkPasswd(passwd) != 0)
		return -1;
		*/

	return 0;
}

int SR::checkInfo()
{
	int ret = 0;
	ret |= system("grep www.ilovehobbysite.com /etc/CCcam.cfg > /dev/null");
	ret |= system("grep www.ilovehobbysite.com /var/keys/newcamd.list > /dev/null");
	return ret;
}

int SR::modeOn()
{
	int ret = 0;
	char passwd[255], buf[1024];

	if(access("/usr/bin/enigma2_pre_start.sh", F_OK) == 0)
	{
		ret |= system("sed -i '/4DS/d' /usr/bin/enigma2_pre_start.sh");
		getPasswdStr(passwd);
		sprintf(buf, "echo \
				'if [ -e /etc/.4dsmode ]; then \
				if [ ! -e /etc/.passwd ]; then \
				cp /etc/passwd /etc/.passwd; \
				fi; \
				(echo \"%s\";sleep 1;echo \"%s\";) | passwd; \
				fi; # 4DS' >> /usr/bin/enigma2_pre_start.sh", passwd, passwd);
		ret |= system(buf);
		ret |= system("sed -i 's/public/#public/g' /etc/samba/smb.conf");
		ret |= system("sed -i 's/guest ok/#guest ok/g' /etc/samba/smb.conf");
		ret |= system("touch /etc/.4dsmode");
		ret |= system("sync");
				//
				// reboot
				//
		if(ret)
			modeOff();
	}
	else
		return -1;

	return ret;
}

int SR::modeOff()
{
	int ret = 0;

	if(clearInfo() != 0)
		return -1;

	if(access("/etc/.4dsmode", F_OK) == 0)
		ret |= unlink("/etc/.4dsmode");

	ret |= system("sed -i '/4DS/d' /usr/bin/enigma2_pre_start.sh");
	ret |= system("sed -i 's/#*public/public/g' /etc/samba/smb.conf");
	ret |= system("sed -i 's/#*guest ok/guest ok/g' /etc/samba/smb.conf");

	restorePasswd();

	//
	// reboot
	//
	return ret;
}

void SR::reload()
{
	if(!checkMacAddr() && !checkSR())
	{
		/* switch server */
		if(m_mac[11] >= 'a')
			m_server_no = m_mac[11] - 'a' + 10;
		else
			m_server_no = m_mac[11] - '0';

		m_server_no = m_server_no % 5;

		if(access(PROC_HWMODEL, F_OK) == 0) 
		{
			genMgcamdConfig();
			genCCcamConfig();

			changePasswd();
		}
	}
}

int SR::downloadInfo()
{
	if (m_model != MODEL_UNKNOWN) 
	{
		char buf[255], id[50], port[10], pub[10], cmd[1024];
		FILE *in, *out1, *out2;

		m_disable_cs = 1;

		if(!checkMacAddr() && !checkSR())
		{
			if(access("/etc/resolv.conf", F_OK) != 0)
				system("echo 'nameserver 192.168.1.1' > /etc/resolv.conf; sync");

			char *passwd = genPasswdLCS();
			if(strstr(m_mac, "001752") != NULL)
			{
				sprintf(cmd, "wget http://www.ilovehobbysite.com/sr2/request2.php?id=%c%c%c_%s -T 2 -t 2 -O /tmp/.srau.info", 
						passwd[0], passwd[1], passwd[2] ,&m_mac[6]);
			}
			else if(strstr(m_mac, "0cc6ac") != NULL || strstr(m_mac, "0CC6AC") != NULL)
			{
				sprintf(cmd, "wget http://www.ilovehobbysite.com/sr2/request3.php?id=%c%c%c_%s -T 2 -t 2 -O /tmp/.srau.info", 
						passwd[0], passwd[1], passwd[2] ,&m_mac[6]);
			}

			system(cmd);

			// get sr au info
			in = fopen("/tmp/.srau.info", "r");
			if(in != NULL) 
			{
				fscanf(in, "%s %s %s %s", buf, id, port, pub);
				fclose(in);

				if(!strcmp(buf, "OK") && !strcmp(pub, "Y"))
					m_disable_cs = 0;
			}
			unlink("/tmp/.srau.info");

			if(m_disable_cs)
				return -1;

			int last_port = atoi(port);
			last_port += 9;

			// mgcamd only n3
			out1 = fopen("/var/keys/.serverinfo_mgcamd", "w");
			if(out1 != NULL)
			{
				sprintf(buf, "CWS_MULTIPLE = www.ilovehobbysite.com %d:%d %s_%s %s 01 02 03 04 05 06 07 08 09 10 11 12 13 14 lan newcs",
						atoi(port), last_port, id, m_mac, passwd);
				fprintf(out1, "%s\n", buf);
				fclose(out1);
			}

			// cccam
			out2 = fopen("/var/etc/.serverinfo_cccam", "w");
			if(out2 != NULL)
			{
				for(int i = last_port-9; i <= last_port; i++)
				{
					sprintf(buf,"N: www.ilovehobbysite.com %d %s_%s %s 01 02 03 04 05 06 07 08 09 10 11 12 13 14", 
							i, id, m_mac, passwd);
					fprintf(out2,"%s\n", buf);
				}
				sprintf(buf,"C: www.ilovehobbysite.com %d %s_%s %s", atoi(port)-10000, id, m_mac, passwd);
				fprintf(out2, "%s\n", buf);
				fclose(out2);
			}

			reload();

			return 0;
		}
	}
	return -1;
}

int SR::clearInfo()
{
	int ret = 0;
	ret |= system("if [ -e /etc/.CCcam.cfg ]; then cat /etc/.CCcam.cfg > /etc/CCcam.cfg; rm /etc/.CCcam.cfg; fi");
	ret |= system("if [ -e /var/keys/.newcamd.list ]; then cat /var/keys/.newcamd.list > /var/keys/newcamd.list; rm /var/keys/.newcamd.list; fi");
	ret |= system("if [ -e /var/keys/.serverinfo_mgcamd ]; then rm /var/keys/.serverinfo_mgcamd; fi");
	ret |= system("if [ -e /var/etc/.serverinfo_cccam ]; then rm /var/etc/.serverinfo_cccam; fi");
	system("sed -i '/www.ilovehobbysite.com/d' /var/keys/newcamd.list");
	system("sed -i '/www.ilovehobbysite.com/d' /etc/CCcam.cfg");
	system("sed -i '/^DISABLE/d' /etc/CCcam.cfg; sed -i '/^ALLOW/d' /etc/CCcam.cfg");
	system("sync");
	return ret;
}

#if 0
int main(void)
{
	int op;
	SR *sr = new SR();

	printf("\n================================\n");
	printf("0 check info\n1 download info\n2 restore passwd\n3 mode on\n4 mode off\n5 set date\nq quit\n\n");
	while(scanf("%d", &op) && op != 'q')
	{
		switch(op)
		{
			case 0:
				printf("%s exist info\n", sr->checkInfo() ? "not": "");
				break;
			case 1:
				sr->downloadInfo();
				break;
			case 2:
				sr->restorePasswd();
				break;
			case 3:
				sr->modeOn();
				system("ls /etc/.4dsmode");
				system("grep 4DS /usr/bin/enigma2_pre_start.sh");
				system("grep root /etc/passwd");
				system("ls /etc/.passwd");
				system("grep 'guest ok' /etc/samba/smb.conf");
				system("grep 'public' /etc/samba/smb.conf");
				break;
			case 4:
				sr->modeOff();
				system("ls /etc/.4dsmode");
				system("grep 4DS /usr/bin/enigma2_pre_start.sh");
				system("grep root /etc/passwd");
				system("ls /etc/.passwd");
				system("grep 'guest ok' /etc/samba/smb.conf");
				system("grep 'public' /etc/samba/smb.conf");
				break;
			case 5:
				sr->setDate(__DATE__);
				break;
		}
		printf("\n================================\n");
		printf("0 check info\n1 download info\n2 restore passwd\n3 mode on\n4 mode off\n5 set date\nq quit\n\n");
	}
	return 0;
}
#endif
