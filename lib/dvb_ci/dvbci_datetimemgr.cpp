/* DVB CI DateTime Manager */

#include <lib/base/eerror.h>
#include <lib/dvb_ci/dvbci_datetimemgr.h>

int eDVBCIDateTimeSession::receivedAPDU(const unsigned char *tag,const void *data, int len)
{
	eDebugNoNewLine("SESSION(%d)/DATETIME %02x %02x %02x: ", session_nb, tag[0],tag[1], tag[2]);
	for (int i=0; i<len; i++)
		eDebugNoNewLine("%02x ", ((const unsigned char*)data)[i]);
	eDebug("");

	if ((tag[0]==0x9f) && (tag[1]==0x84))
	{
		switch (tag[2])
		{
		case 0x40:
			state=stateSendDateTime;
			return 1;
			break;
		default:
			eDebug("unknown APDU tag 9F 84 %02x", tag[2]);
			break;
		}
	}
	return 0;
}

int eDVBCIDateTimeSession::doAction()
{
	switch (state)
	{
	case stateStarted:
		return 0;
	case stateSendDateTime:
	{

		/* sidabary-ciplus-ntvplus */
		extern time_t getRTC();
	
		unsigned char tag[3]={0x9f, 0x84, 0x41}; // date_time_response
		unsigned char msg[7]={0, 0, 0, 0, 0, 0, 0};

		/* sidabary-ciplus-ntvplus */
		int	date_y,date_m,date_d,time_h,time_m,time_s;
		int	mjd,L;
		
		struct	tm	*struct_time;	
		time_t	cur_time = getRTC();

		/* rtc time not use. */
        if ( cur_time == 0 )
            cur_time = time(0);

		/* get current local time from RTC time_t value */
		struct_time = localtime(&cur_time);
		date_y = struct_time->tm_year;
		date_m = struct_time->tm_mon + 1;
		date_d = struct_time->tm_mday;
		time_h = struct_time->tm_hour;
		time_m = struct_time->tm_min;
		time_s = struct_time->tm_sec;

		/* calculate MJD from  yy-mm-dd */		
		if(date_m == 1 || date_m == 2)
			L = 1;
		else
			L = 0;
		mjd = 14956 + date_d + (int)((date_y - L) * 365.25f) + ((date_m + 1 + (L * 12)) * 30.6001f);
		
		/* take 16LSB of MJD and convert to 4bit BCD type */
		/* ignore local offset */
		msg[0] =  (unsigned char)((mjd & 0x0000ff00) >> 8);
		msg[1] =  (unsigned char)(mjd & 0x000000ff);
		msg[2] =  (unsigned char)((time_h / 10) << 4);
		msg[2] |= (unsigned char)(time_h % 10);
		msg[3] =  (unsigned char)((time_m / 10) << 4);
		msg[3] |= (unsigned char)(time_m % 10);
		msg[4] =  (unsigned char)((time_s / 10) << 4);
		msg[4] |= (unsigned char)(time_s % 10);

		eDebug("[%02x%02x%02x%02x%02x]",msg[0],msg[1],msg[2],msg[3],msg[4]);
		
		sendAPDU(tag, msg, 7);
		return 0;
	}
	case stateFinal:
		eDebug("stateFinal und action! kann doch garnicht sein ;)");
	default:
		return 0;
	}
}
