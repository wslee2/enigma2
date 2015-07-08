#ifndef __SR_H_
#define __SR_H_

class AutoPasswd
{
	public:
		AutoPasswd();
		~AutoPasswd();
		static AutoPasswd *getInstance();

		char* getMacAddr(const char *device = "eth0");
		int checkPasswd(const char *oldPasswd, const char *passwdFile = "/etc/passwd");
		void setDate(const char *date);
		void restorePasswd(void);
		void changePasswd(void);

	protected:
		char m_date[32];
		char m_mac[64];
		char m_passwd[64];

		int checkMacAddr();
		int getPasswdStr(char *passwd);

	private:
		static AutoPasswd *instance;

		void genPasswd();
};

class SR : public AutoPasswd
{
	public:
		SR();
		~SR();
		static SR *getInstance();

		int downloadInfo();
		int checkInfo();
		int clearInfo();
		void reload();
		int modeOn();
		int modeOff();

	private:
		static SR *instance;
		int m_server_no;
		int m_disable_cs;

		enum { MODEL_UNKNOWN, 
			MODEL_TMTWIN, 
			MODEL_TM2T, 
			MODEL_TMSINGLE,
			MODEL_TMNANO,
			MODEL_TMNANO2T,
			MODEL_IOS100HD, 
			MODEL_IOS200HD, 
			MODEL_IOS300HD,
			MODEL_TMNANO2SUPER,
			MODEL_FORCE1,
			MODEL_FORCE1PLUS
		};

		int m_model;

		char* genPasswdLCS();

		void genMgcamdConfig();
		void genCCcamConfig();

		int checkSR();
};

#endif
