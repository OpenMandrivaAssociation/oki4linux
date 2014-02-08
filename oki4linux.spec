Summary:	Drivers for Oki 4w, oki 400w and okipage 4w plus GDI winprinters
Name:		oki4linux
Version:	2.1gst
Release:	15
License:	GPL
Group:		System/Printing
URL:		http://www.linuxprinting.org/download/printing/
Source0:	http://www.linuxprinting.org/download/printing/oki4linux-2.1gst.tar.gz
Source1:	oki4daemon.init
Source2:	README.OKI-Winprinters
Patch0:		oki4linux-2.0-daemon-mdk-patch
Patch1:		oki4linux-2.1gst-LDFLAGS.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A Linux / UNIX driver for the  okipage 4w, oki 400w and
okipage 4w plus GDI printers,

%prep

%setup -q -n %{name}
%patch0 -p1
%patch1 -p0

# Do some small corrections in the daemon script:
# - The daemon crashes with "setlogsock('unix');"
# - Correct the path for the driver
pushd src
mv oki4daemon oki4daemon.pre
sed "s/setlogsock('unix');/setlogsock('inet');/" oki4daemon.pre | sed "s:/usr/local/sbin/oki4drv:/usr/bin/oki4drv:" > oki4daemon
popd

cp %{SOURCE1} oki4daemon.init
cp %{SOURCE2} README.OKI-Winprinters

%build
pushd src
make clean
%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1

pushd src
# Program files
install -m0755 oki4drv %{buildroot}%{_bindir}
install -m0755 oki4daemon %{buildroot}%{_sbindir}
install -m0644 oki4drv.man %{buildroot}%{_mandir}/man1/oki4drv.1
popd

install -m0755 oki4daemon.init %{buildroot}%{_initrddir}/oki4daemon

%post
%_post_service oki4daemon
# Restart the oki4daemon when it is running, but do not activate it by
# default. It blocks the parallel port for non-OKI devices.
if [ "$1" -ne "1" ]; then
    # On update
    service oki4daemon condrestart > /dev/null 2>/dev/null || :
else
    # Turn it off, as printerdrake will enable it if used.
    # Otherwise this will make printerdrake pop up every boote
    chkconfig --level 2345 oki4daemon off
fi

%preun
#Stop oki4daemon when uninstalling printer-filters
%_preun_service oki4daemon

%postun
if [ "$1" -ge "1" ]; then
    # On update
    /sbin/service oki4daemon condrestart >/dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README.OKI-Winprinters COPYING ChangeLog README
%doc doc samples src/README.oki4daemon src/align.ps
%attr(0755,root,root) %{_initrddir}/oki4daemon
%attr(0755,root,root) %{_sbindir}/oki4daemon
%attr(0755,root,root) %{_bindir}/oki4drv
%attr(0644,root,root) %{_mandir}/man1/oki4drv.1*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-13mdv2011.0
+ Revision: 666941
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-12mdv2011.0
+ Revision: 607007
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-11mdv2010.1
+ Revision: 519048
- rebuild

* Thu Aug 06 2009 Eugeni Dodonov <eugeni@mandriva.com> 2.1gst-10mdv2010.0
+ Revision: 410920
- Updated init script to be LSB-compliant.

* Thu Dec 25 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-9mdv2009.1
+ Revision: 319130
- use %%ldflags (P1)

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1gst-8mdv2009.0
+ Revision: 223358
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-7mdv2008.1
+ Revision: 179107
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Sep 06 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-6mdv2008.0
+ Revision: 80681
- fix #33200 (Upgrade/install of oki4linux post script issue a warning and fail : --off: option iconnue)

* Wed Sep 05 2007 Marcelo Ricardo Leitner <mrl@mandriva.com> 2.1gst-5mdv2008.0
+ Revision: 80016
- Do not start the service by default. Closes: #33128
  Otherwise, it will force parport module load, which triggers an udev event,
  which triggers printerdrake.

* Thu Aug 30 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-4mdv2008.0
+ Revision: 75349
- fix deps (pixel)

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-3mdv2008.0
+ Revision: 64168
- use the new System/Printing RPM GROUP

* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-2mdv2008.0
+ Revision: 61096
- rebuild

* Fri Aug 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-1mdv2008.0
+ Revision: 60985
- Import oki4linux



* Thu Aug 09 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1gst-1mdv2008.0
- initial Mandriva package

* Tue May 18 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-05-18 17:36:07 (60763)
- Added /dev/oki4drv to the package. The daemon creates if not found,
  but with wrong permissions.
- Cleanup at %%files section.

* Thu Jan 15 2004 Marcelo Ricardo Leitner <mrl@conectiva.com.br>
+ 2004-01-15 16:07:26 (44866)
- New upstream: 2.1gst
- Removed already-in-code patch: daemon
- Removed old menu support.

* Wed Mar 12 2003 Andreas Hasenack <andreas@conectiva.com.br>
+ 2003-03-12 11:42:08 (27272)
- if first install, add the daemon to ntsysv (but disabled)
- added chkconfig to prereq
- Closes: #7923
- the above is just for reference, that bug is already closed

* Thu Aug 29 2002 Gustavo Niemeyer <niemeyer@conectiva.com>
+ 2002-08-29 18:33:20 (8945)
- Imported package from 8.0.
