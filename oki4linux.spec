Summary:	Drivers for Oki 4w, oki 400w and okipage 4w plus GDI winprinters
Name:		oki4linux
Version:	2.0
Release:	2
License:	GPL
Group:		System/Printing
URL:		http://www.linuxprinting.org/download/printing/
Source0:	http://www.linuxprinting.org/download/printing/oki4linux-2.1gst.tar.gz
Source1:	oki4daemon.service
Source2:	README.OKI-Winprinters
Patch0:		oki4linux-2.0-daemon-mdk-patch
Patch1:		oki4linux-2.1gst-LDFLAGS.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

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

cp %{SOURCE1} oki4daemon.service
cp %{SOURCE2} README.OKI-Winprinters

%build
pushd src
make clean
%make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"
popd

%install

install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man1

pushd src
# Program files
install -m0755 oki4drv %{buildroot}%{_bindir}
install -m0755 oki4daemon %{buildroot}%{_sbindir}
install -m0644 oki4drv.man %{buildroot}%{_mandir}/man1/oki4drv.1
popd

install -m0755 oki4daemon.service %{buildroot}%{_unitdir}/oki4daemon.service

%post
%systemd_post oki4daemon.service

%preun
%systemd_preun oki4daemon.service

%postun
%systemd_postun_with_restart oki4daemon.service

%files
%defattr(0644,root,root,0755)
%doc README.OKI-Winprinters COPYING ChangeLog README
%doc doc samples src/README.oki4daemon src/align.ps
%{_unitdir}/oki4daemon.service
%attr(0755,root,root) %{_sbindir}/oki4daemon
%attr(0755,root,root) %{_bindir}/oki4drv
%attr(0644,root,root) %{_mandir}/man1/oki4drv.1*
