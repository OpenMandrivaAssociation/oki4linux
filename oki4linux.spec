Summary:	Drivers for Oki 4w, oki 400w and okipage 4w plus GDI winprinters
Name:		oki4linux
Version:	2.1gst
Release:	%mkrel 6
License:	GPL
Group:		System/Printing
URL:		http://www.linuxprinting.org/download/printing/
Source0:	http://www.linuxprinting.org/download/printing/oki4linux-2.1gst.tar.gz
Source1:	oki4daemon.init
Source2:	README.OKI-Winprinters
Patch0:		oki4linux-2.0-daemon-mdk-patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007

%description
A Linux / UNIX driver for the  okipage 4w, oki 400w and
okipage 4w plus GDI printers,

%prep

%setup -q -n %{name}
%patch0 -p1

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
%make CFLAGS="%{optflags}"
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
