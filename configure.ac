AC_INIT([enigma2],[3.0.0],[enigma2-devel@lists.elitedvb.net])
AM_INIT_AUTOMAKE([dist-bzip2 no-define tar-pax -Wno-portability])
AC_CONFIG_HEADERS([enigma2_config.h])

# Silent rules are available since 1.11, but older versions
# are still in use. So don't use them unconditionally.
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])

AC_USE_SYSTEM_EXTENSIONS
AC_SYS_LARGEFILE

AC_PROG_CC
AC_PROG_CXX
m4_ifdef([LT_INIT], [LT_INIT], [AC_PROG_LIBTOOL])
AC_CONFIG_MACRO_DIR([m4])
AC_OPENMP()

AC_PATH_PROG(MSGFMT, msgfmt, AC_MSG_ERROR(Could not find msgfmt))

AM_PATH_PYTHON
AX_PYTHON_DEVEL
AX_PKG_SWIG
AX_SWIG_ENABLE_CXX
AX_SWIG_PYTHON
AX_PTHREAD

TUXBOX_APPS_DVB

AM_CONDITIONAL(HAVE_GIT_DIR, test -d "$srcdir/.git")
AM_CONDITIONAL(HAVE_FAKE_GIT_DIR, test -f "$srcdir/.git/last_commit_info")

dnl versions of gstreamer and plugins-base
AC_ARG_WITH(gstversion,
	AS_HELP_STRING([--with-gstversion],[use gstreamer version (major.minor)]),
	[GST_MAJORMINOR=$withval],[GST_MAJORMINOR=0.10])

PKG_CHECK_MODULES(BASE, [freetype2 fribidi gstreamer-$GST_MAJORMINOR gstreamer-pbutils-$GST_MAJORMINOR libdvbsi++ libpng libxml-2.0 sigc++-1.2 libssl libcrypto])
PKG_CHECK_MODULES(LIBDDVD, libdreamdvd, HAVE_LIBDDVD="yes", HAVE_LIBDDVD="no")
AM_CONDITIONAL(HAVE_LIBDDVD, test "$HAVE_LIBDDVD" = "yes")

AC_CHECK_LIB([dl], [dlopen], [LIBDL_LIBS="-ldl"], [AC_MSG_ERROR([Could not find libdl])])
AC_SUBST(LIBDL_LIBS)
AC_CHECK_LIB([jpeg], [jpeg_set_defaults], [LIBJPEG_LIBS="-ljpeg"], [AC_MSG_ERROR([Could not find libjpeg])])
AC_SUBST(LIBJPEG_LIBS)
AC_CHECK_LIB([ungif], [DGifOpen], [LIBGIF_LIBS="-lungif"], [AC_CHECK_LIB([gif], [DGifOpen], [LIBGIF_LIBS="-lgif"], [AC_MSG_ERROR([Could not find libgif or libungif])])])
AC_SUBST(LIBGIF_LIBS)

AC_LANG_PUSH([C++])
AC_CHECK_LIB([xmlccwrap], [exit], [LIBXMLCCWRAP_LIBS="-lxmlccwrap"], [AC_MSG_ERROR([Could not find libxmlccwrap])])
AC_SUBST(LIBXMLCCWRAP_LIBS)
AC_LANG_POP

AC_ARG_WITH(boxtype,
	[  --with-boxtype=NAME box type [[none,dm7025,dm800...]]],
	[BOXTYPE="$withval"],[BOXTYPE="dm800"])
AC_SUBST(BOXTYPE)
AC_DEFINE_UNQUOTED(BOXTYPE,"$BOXTYPE",[box type])

AM_CONDITIONAL(DREAMBOX, test `echo "$BOXTYPE" | cut -b 1-2` == "dm")

AM_CONDITIONAL(HAVE_TEMPFANCONTROL, test "$BOXTYPE" == dm8000 -o "$BOXTYPE" == dm800se -o "$BOXTYPE" == dm500hd )
if test `echo "$BOXTYPE" | cut -b 1-2` == "dm"; then

	AC_DEFINE(DREAMBOX, 1, [Dreambox hardware])
	AC_DEFINE(KEY_PLAY_ACTUALLY_IS_KEY_PLAYPAUSE, 1,[define when rc sends a KEY_PLAY event for its KEY_PLAYPAUSE key])
fi
if test "$BOXTYPE" == "vusolo2" -o "$BOXTYPE" == "vuduo2"; then
	AC_DEFINE(VUPLUS_RC_WORKAROUND, 1, [workaround for problem with vusolo2/vuduo2 event/rc driver])
fi

AC_ARG_WITH(textlcd,
	AC_HELP_STRING([--with-textlcd], [use ascii based lcd, yes or no]),
	[[withtextlcd=$withval]],
	[[withtextlcd=no]]
)
if test x"$withtextlcd" != xno ; then
	AC_DEFINE(HAVE_TEXTLCD, 1,[Define when using an ascii based lcd device])
fi
AM_CONDITIONAL(HAVE_TEXTLCD, test x"$withtextlcd" != xno)

AC_ARG_WITH(colorlcd,
	AC_HELP_STRING([--with-colorlcd], [use 96x64 16bpp color display, yes or no]),
	[[withcolorlcd=$withval]],
	[[withcolorlcd=no]]
)
if test x"$withcolorlcd" != xno ; then
	AC_DEFINE(HAVE_COLORLCD, 1,[Define when using a 96x64 color display device])
fi
AM_CONDITIONAL(HAVE_COLORLCD, test x"$withcolorlcd" != xno)


AC_ARG_WITH(oldpvr,
	AC_HELP_STRING([--with-oldpvr], [use /dev/misc/pvr instead of /dev/dvb/adapterX/dvrX, yes or no]),
	[[witholdpvr=$withval]],
	[[witholdpvr=no]]
)
if test x"$witholdpvr" != xno ; then
	AC_DEFINE(HAVE_OLDPVR, 1,[Define when using /dev/misc/pvr])
fi
AM_CONDITIONAL(HAVE_OLDPVR, test x"$witholdpvr" != xno)

if test `echo "$BOXTYPE" | cut -b 1-2` == "vu"; then
    AC_DEFINE(KEY_F1_TO_KEY_PC, 1,[define when rc sends a KEY_F1 event for its KEY_PC key])
    AC_DEFINE(KEY_F5_TO_KEY_ANGLE, 1,[define when rc sends a KEY_F5 event for its KEY_ANGLE key])
    AC_DEFINE(KEY_DOT_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_DOT event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_HOME_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_HOME event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_MEDIA_TO_KEY_KEY_F2, 1,[define when rc sends a KEY_MEDIA event for its KEY_KEY_F1 key])
    AC_DEFINE(HAVE_LINUXSOCKADDR, 1,[define it use sockaddr_un instead of sockaddr_in on linux domain socket.])
    AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
    AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
    AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
fi
if test `echo "$BOXTYPE" | cut -b 1-2` == "tm"; then
    AC_DEFINE(KEY_F1_TO_KEY_PC, 1,[define when rc sends a KEY_F1 event for its KEY_PC key])
    AC_DEFINE(KEY_F5_TO_KEY_ANGLE, 1,[define when rc sends a KEY_F5 event for its KEY_ANGLE key])
    AC_DEFINE(KEY_DOT_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_DOT event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_HOME_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_HOME event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_MEDIA_TO_KEY_KEY_F2, 1,[define when rc sends a KEY_MEDIA event for its KEY_KEY_F1 key])
    AC_DEFINE(HAVE_LINUXSOCKADDR, 1,[define it use sockaddr_un instead of sockaddr_in on linux domain socket.])
    AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
    AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
    AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
fi
if test `echo "$BOXTYPE" | cut -b 1-3` == "ios"; then
    AC_DEFINE(KEY_F1_TO_KEY_PC, 1,[define when rc sends a KEY_F1 event for its KEY_PC key])
    AC_DEFINE(KEY_F5_TO_KEY_ANGLE, 1,[define when rc sends a KEY_F5 event for its KEY_ANGLE key])
    AC_DEFINE(KEY_DOT_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_DOT event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_HOME_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_HOME event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_MEDIA_TO_KEY_KEY_F2, 1,[define when rc sends a KEY_MEDIA event for its KEY_KEY_F1 key])
    AC_DEFINE(HAVE_LINUXSOCKADDR, 1,[define it use sockaddr_un instead of sockaddr_in on linux domain socket.])
    AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
    AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
    AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
fi
if test `echo "$BOXTYPE" | cut -b 1-2` == "op"; then
    AC_DEFINE(KEY_F1_TO_KEY_PC, 1,[define when rc sends a KEY_F1 event for its KEY_PC key])
    AC_DEFINE(KEY_F5_TO_KEY_ANGLE, 1,[define when rc sends a KEY_F5 event for its KEY_ANGLE key])
    AC_DEFINE(KEY_DOT_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_DOT event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_HOME_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_HOME event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_MEDIA_TO_KEY_KEY_F2, 1,[define when rc sends a KEY_MEDIA event for its KEY_KEY_F1 key])
    AC_DEFINE(HAVE_LINUXSOCKADDR, 1,[define it use sockaddr_un instead of sockaddr_in on linux domain socket.])
    AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
    AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
    AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
fi
if test `echo "$BOXTYPE" | cut -b 1-5` == "force"; then
    AC_DEFINE(KEY_F1_TO_KEY_PC, 1,[define when rc sends a KEY_F1 event for its KEY_PC key])
    AC_DEFINE(KEY_F5_TO_KEY_ANGLE, 1,[define when rc sends a KEY_F5 event for its KEY_ANGLE key])
    AC_DEFINE(KEY_DOT_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_DOT event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_HOME_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_HOME event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_MEDIA_TO_KEY_KEY_F2, 1,[define when rc sends a KEY_MEDIA event for its KEY_KEY_F1 key])
    AC_DEFINE(HAVE_LINUXSOCKADDR, 1,[define it use sockaddr_un instead of sockaddr_in on linux domain socket.])
    AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
    AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
    AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
fi
if test `echo "$BOXTYPE" | cut -b 1-5` == "media"; then
    AC_DEFINE(KEY_F1_TO_KEY_PC, 1,[define when rc sends a KEY_F1 event for its KEY_PC key])
    AC_DEFINE(KEY_F5_TO_KEY_ANGLE, 1,[define when rc sends a KEY_F5 event for its KEY_ANGLE key])
    AC_DEFINE(KEY_DOT_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_DOT event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_HOME_TO_KEY_HOMEPAGE, 1,[define when rc sends a KEY_HOME event for its KEY_KEY_HOMEPAGE key])
    AC_DEFINE(KEY_MEDIA_TO_KEY_KEY_F2, 1,[define when rc sends a KEY_MEDIA event for its KEY_KEY_F1 key])
    AC_DEFINE(HAVE_LINUXSOCKADDR, 1,[define it use sockaddr_un instead of sockaddr_in on linux domain socket.])
    AC_DEFINE(FORCE_NO_BLENDING_ACCELERATION, 1,[define when the framebuffer acceleration does not have alphablending support, though the autodetection might indicate that it does])
    AC_DEFINE(FORCE_ADVANCED_REMOTE, 1,[define to fixup the input device identification when the remote control is actually an 'advanced' remote (with play/forward/rewind keys)])
    AC_DEFINE(FORCE_NO_FILL_ACCELERATION, 1,[define when the framebuffer acceleration does not have fill support])
fi

AC_ARG_WITH(libsdl,
	AS_HELP_STRING([--with-libsdl],[use libsdl, yes or no]),
	[with_libsdl=$withval],[with_libsdl=no])
if test "$with_libsdl" = "yes"; then
	PKG_CHECK_MODULES(LIBSDL, sdl)
fi
AM_CONDITIONAL(HAVE_LIBSDL, test "$with_libsdl" = "yes")

AC_ARG_WITH(libxine,
	AS_HELP_STRING([--with-libxine],[use libxine, yes or no]),
	[with_libxine=$withval],[with_libxine=no])
if test "$with_libxine" = "yes"; then
	PKG_CHECK_MODULES(LIBXINE, libxine)
	AC_DEFINE([WITH_XINE],[1],[Define to 1 if you have libxine])
fi
AM_CONDITIONAL(HAVE_LIBXINE, test "$with_libxine" = "yes")

AC_ARG_WITH(debug,
	AS_HELP_STRING([--without-debug],[disable debugging code]),
	[with_debug="$withval"],[with_debug="yes"])
if test "$with_debug" = "yes"; then
	DEBUG_CFLAGS="-ggdb3"
	AC_DEFINE([DEBUG],[1],[Define to 1 to enable debugging code])
fi

AC_ARG_WITH(memcheck,
	AS_HELP_STRING([--with-memcheck],[enable memory leak checks]),
	[with_memcheck="$withval"],[with_memcheck="no"])
if test "$with_memcheck" = "yes"; then
	AC_DEFINE([MEMLEAK_CHECK],[1],[Define to 1 to enable memory leak checks])
fi

AC_ARG_WITH(po,
	AS_HELP_STRING([--with-po],[enable updating of po files]),
	[with_po="$withval"],[with_po="no"])
if test "$with_po" = "yes"; then
	AC_PATH_PROG(MSGINIT, msginit)
	AC_PATH_PROG(MSGMERGE, msgmerge)
	AC_PATH_PROG(MSGUNIQ, msguniq)
	AC_PATH_PROG(XGETTEXT, xgettext)
	if test -z "$MSGINIT" -o -z "$MSGMERGE" -o -z "$MSGUNIQ" -o -z "$XGETTEXT"; then
		AC_MSG_ERROR([Could not find required gettext tools])
	fi
fi
AM_CONDITIONAL(UPDATE_PO, test "$with_po" = "yes")

ENIGMA2_CFLAGS="-fno-rtti -fno-exceptions"
AC_SUBST(ENIGMA2_CFLAGS)

CPPFLAGS="$CPPFLAGS $PYTHON_CPPFLAGS"
CFLAGS="$CFLAGS $DEBUG_CFLAGS -Wall"
CXXFLAGS="$CXXFLAGS $DEBUG_CFLAGS -Wall $BASE_CFLAGS $ENIGMA2_CFLAGS $PTHREAD_CFLAGS $OPENMP_CFLAGS"

AC_CONFIG_FILES([
Makefile
data/Makefile
data/fonts/Makefile
data/countries/Makefile
data/extensions/Makefile
data/keymaps/Makefile
data/hw_info/Makefile
data/rc_models/Makefile
data/skin_default/Makefile
data/skin_default/menu/Makefile
data/skin_default/icons/Makefile
data/skin_default/buttons/Makefile
data/skin_default/spinner/Makefile
data/skin_default/LCDIcons/Makefile
include/Makefile
lib/Makefile
lib/base/eenv.cpp
lib/python/Makefile
lib/python/Components/Makefile
lib/python/Components/Converter/Makefile
lib/python/Components/Renderer/Makefile
lib/python/Components/Sources/Makefile
lib/python/Screens/Makefile
lib/python/Plugins/Makefile
lib/python/Plugins/SystemPlugins/CableScan/Makefile
lib/python/Plugins/SystemPlugins/FastScan/Makefile
lib/python/Plugins/SystemPlugins/OSDPositionSetup/Makefile
lib/python/Plugins/SystemPlugins/OSD3DSetup/Makefile
lib/python/Plugins/SystemPlugins/HdmiCEC/Makefile
lib/python/Plugins/SystemPlugins/VideoClippingSetup/Makefile
lib/python/Plugins/Extensions/iSettingE2/Makefile
lib/python/Plugins/Extensions/iSettingE2/Conf/Makefile
lib/python/Plugins/Extensions/iSettingE2/Conf/mips/Makefile
lib/python/Plugins/Extensions/iSettingE2/Fonts/Makefile
lib/python/Plugins/Extensions/iSettingE2/Icons/Makefile
lib/python/Plugins/Extensions/iSettingE2/Icons/VirtualKB/Makefile
lib/python/Plugins/Extensions/iSettingE2/Buttons/Makefile
lib/python/Plugins/Extensions/iSettingE2/Skins/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/fr/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/fr/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/it/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/it/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/de/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/de/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/en/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/en/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/lv/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/lv/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/es/Makefile
lib/python/Plugins/Extensions/iSettingE2/po/es/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CutListEditor/Makefile
lib/python/Plugins/Extensions/CutListEditor/meta/Makefile
lib/python/Plugins/Extensions/DVDBurn/Makefile
lib/python/Plugins/Extensions/DVDBurn/meta/Makefile
lib/python/Plugins/Extensions/DVDPlayer/Makefile
lib/python/Plugins/Extensions/DVDPlayer/meta/Makefile
lib/python/Plugins/Extensions/GraphMultiEPG/Makefile
lib/python/Plugins/Extensions/GraphMultiEPG/meta/Makefile
lib/python/Plugins/Extensions/Makefile
lib/python/Plugins/Extensions/MediaPlayer/Makefile
lib/python/Plugins/Extensions/MediaPlayer/meta/Makefile
lib/python/Plugins/Extensions/MediaScanner/Makefile
lib/python/Plugins/Extensions/MediaScanner/meta/Makefile
lib/python/Plugins/Extensions/Modem/Makefile
lib/python/Plugins/Extensions/PicturePlayer/Makefile
lib/python/Plugins/Extensions/PicturePlayer/meta/Makefile
lib/python/Plugins/Extensions/PicturePlayer/data/Makefile
lib/python/Plugins/Extensions/SocketMMI/Makefile
lib/python/Plugins/Extensions/SocketMMI/meta/Makefile
lib/python/Plugins/Extensions/SocketMMI/src/Makefile
lib/python/Plugins/Extensions/TuxboxPlugins/Makefile
lib/python/Plugins/Extensions/TuxboxPlugins/meta/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/Cool3D/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/Cool3D/Menu/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/Cool3D/MyDesign/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/Cool3D/Standard/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/CoolSkin/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/bg/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/bg/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/cs/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/cs/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/de/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/de/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/fa/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/fa/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/fr/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/fr/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/it/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/it/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/nl/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/nl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/no/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/no/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/pl/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/pl/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/ru/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/ru/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/sk/Makefile
lib/python/Plugins/Extensions/CoolTVGuide/locale/sk/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/MyTube/Makefile
lib/python/Plugins/Extensions/MyTube/img/Makefile
lib/python/Plugins/Extensions/MyTube/locale/Makefile
lib/python/Plugins/Extensions/MyTube/locale/ru/Makefile
lib/python/Plugins/Extensions/MyTube/locale/ru/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/MyTube/skins/Makefile
lib/python/Plugins/Extensions/MyTube/skins/default/Makefile
lib/python/Plugins/Extensions/MyTube/skins/default/MyTube/Makefile
lib/python/Plugins/Extensions/NGsetting/Makefile
lib/python/Plugins/Extensions/NGsetting/Moduli/Makefile
lib/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Makefile
lib/python/Plugins/Extensions/NGsetting/Moduli/NGsetting/Temp/Makefile
lib/python/Plugins/Extensions/NGsetting/Panel/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/es/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/es/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/fr/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/fr/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/it/Makefile
lib/python/Plugins/Extensions/NGsetting/Po/it/LC_MESSAGES/Makefile
lib/python/Plugins/Extensions/NGsetting/Skin/Makefile
lib/python/Plugins/PLi/Makefile
lib/python/Plugins/SystemPlugins/CommonInterfaceAssignment/Makefile
lib/python/Plugins/SystemPlugins/CommonInterfaceAssignment/meta/Makefile
lib/python/Plugins/SystemPlugins/DefaultServicesScanner/Makefile
lib/python/Plugins/SystemPlugins/DefaultServicesScanner/meta/Makefile
lib/python/Plugins/SystemPlugins/DiseqcTester/Makefile
lib/python/Plugins/SystemPlugins/DiseqcTester/meta/Makefile
lib/python/Plugins/SystemPlugins/FrontprocessorUpgrade/Makefile
lib/python/Plugins/SystemPlugins/FrontprocessorUpgrade/meta/Makefile
lib/python/Plugins/SystemPlugins/Hotplug/Makefile
lib/python/Plugins/SystemPlugins/Hotplug/meta/Makefile
lib/python/Plugins/SystemPlugins/Makefile
lib/python/Plugins/SystemPlugins/MountManager/Makefile
lib/python/Plugins/SystemPlugins/MountManager/icons/Makefile
lib/python/Plugins/SystemPlugins/MountManager/locale/Makefile
lib/python/Plugins/SystemPlugins/MountManager/locale/ru/Makefile
lib/python/Plugins/SystemPlugins/MountManager/locale/ru/LC_MESSAGES/Makefile
lib/python/Plugins/SystemPlugins/NetworkWizard/Makefile
lib/python/Plugins/SystemPlugins/NetworkWizard/meta/Makefile
lib/python/Plugins/SystemPlugins/NFIFlash/Makefile
lib/python/Plugins/SystemPlugins/NFIFlash/meta/Makefile
lib/python/Plugins/SystemPlugins/PositionerSetup/Makefile
lib/python/Plugins/SystemPlugins/PositionerSetup/meta/Makefile
lib/python/Plugins/SystemPlugins/SatelliteEquipmentControl/Makefile
lib/python/Plugins/SystemPlugins/SatelliteEquipmentControl/meta/Makefile
lib/python/Plugins/SystemPlugins/Satfinder/Makefile
lib/python/Plugins/SystemPlugins/Satfinder/meta/Makefile
lib/python/Plugins/SystemPlugins/SkinSelector/Makefile
lib/python/Plugins/SystemPlugins/SkinSelector/meta/Makefile
lib/python/Plugins/SystemPlugins/SoftwareManager/Makefile
lib/python/Plugins/SystemPlugins/SoftwareManager/meta/Makefile
lib/python/Plugins/SystemPlugins/TempFanControl/Makefile
lib/python/Plugins/SystemPlugins/TempFanControl/meta/Makefile
lib/python/Plugins/SystemPlugins/VideoEnhancement/Makefile
lib/python/Plugins/SystemPlugins/VideoEnhancement/meta/Makefile
lib/python/Plugins/SystemPlugins/VideoTune/Makefile
lib/python/Plugins/SystemPlugins/VideoTune/meta/Makefile
lib/python/Plugins/SystemPlugins/Videomode/Makefile
lib/python/Plugins/SystemPlugins/Videomode/meta/Makefile
lib/python/Plugins/SystemPlugins/WirelessLan/Makefile
lib/python/Plugins/SystemPlugins/WirelessLan/meta/Makefile
lib/python/Tools/Makefile
po/Makefile
main/Makefile
tools/Makefile
tools/enigma2.sh
enigma2.pc
])
AC_OUTPUT
#lib/python/Plugins/Extensions/MyTube/Makefile
#lib/python/Plugins/Extensions/MyTube/locale/Makefile
#lib/python/Plugins/Extensions/MyTube/locale/ru/Makefile
#lib/python/Plugins/Extensions/MyTube/locale/ru/LC_MESSAGES/Makefile
#lib/python/Plugins/Extensions/MyTube/meta/Makefile
#lib/python/Plugins/Extensions/MyTube/po/Makefile
#data/MetropolisHD/Makefile
#data/MetropolisHD/buttons/Makefile
#data/MetropolisHD/chnsel/Makefile
#data/MetropolisHD/icons/Makefile
#data/MetropolisHD/infobar/Makefile
#data/MetropolisHD/menu/Makefile
#data/MetropolisHD/skin_default/Makefile
#data/MetropolisHD/skin_default/buttons/Makefile
#data/MetropolisHD/skin_default/icons/Makefile

#lib/python/Plugins/Extensions/Epanel/script/Makefile
#lib/python/Plugins/Extensions/Epanel/Makefile
#lib/python/Plugins/Extensions/Epanel/images/Makefile
#lib/python/Plugins/Extensions/Epanel/script/Makefile
#lib/python/Plugins/Extensions/Epanel/locale/Makefile
#lib/python/Plugins/Extensions/Epanel/locale/ru/Makefile
#lib/python/Plugins/Extensions/Epanel/locale/ru/LC_MESSAGES/Makefile
#lib/python/Plugins/Extensions/Epanel/locale/uk/Makefile
#lib/python/Plugins/Extensions/Epanel/locale/uk/LC_MESSAGES/Makefile
#lib/python/Plugins/SystemPlugins/TempFanControl/Makefile
#lib/python/Plugins/SystemPlugins/TempFanControl/meta/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/images/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/cs/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/cs/LC_MESSAGES/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/de/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/de/LC_MESSAGES/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/nl/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/nl/LC_MESSAGES/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/pl/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/pl/LC_MESSAGES/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/ru/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/ru/LC_MESSAGES/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/sl/Makefile
#lib/python/Plugins/PLi/SoftcamSetup/locale/sl/LC_MESSAGES/Makefile
#
