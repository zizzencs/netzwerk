############################################################
# AICCU - Automatic IPv6 Connectivity Client Utility
# by Jeroen Massar <jeroen@sixxs.net>
# (c) Copyright 2003-2005 SixXS
############################################################
# AICCU RPM Spec File
############################################################

Summary:   SixXS Automatic IPv6 Connectivity Client Utility
Name:      aiccu
Version:   2007.01.15
Release:   27%{?dist}
License:   BSD
Group:     System Environment/Daemons
URL:       http://www.sixxs.net/tools/aiccu/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:    http://www.sixxs.net/archive/sixxs/aiccu/unix/aiccu_20070115.tar.gz
Source1:   aiccu.service
Patch0: aiccu-cloexec.patch
Patch1: aiccu-run.patch
Patch2: aiccu-syslog-daemon.patch
#Patch3: aiccu-gnutls34.patch
Patch3: aiccu-setupscript.patch
BuildRequires: gnutls-devel
BuildRequires: systemd-units
Requires:  iproute
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
This client automatically gives one IPv6 connectivity
without having to manually configure interfaces etc.
One does need a SixXS account and at least a tunnel. These
can be freely & gratis requested from the SixXS website.
For more information about SixXS check http://www.sixxs.net

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1 -b .run
%patch2 -p1 -b .syslog-daemon
%patch3 -p1
#%patch4 -p1

# fix executable permissions on non-executable content
# so debuginfo can pick them up properly
find . -type f -not -name rules -and -not -name *init* -exec chmod a-x \{\} \;

%build
make %{?_smp_mflags} RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wno-error"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove old-style init script
rm $RPM_BUILD_ROOT%{_sysconfdir}/init.d/*

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/

%post
%systemd_post aiccu.service

%preun
%systemd_preun aiccu.service

%postun
%systemd_postun_with_restart aiccu.service 

%clean
make clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/README doc/LICENSE
%{_sbindir}/aiccu
# aiccu.conf contains the users's SixXS password, so don't
# make it readable by non-root
%attr(600, root,root) %config(noreplace) %{_sysconfdir}/aiccu.conf
%{_unitdir}/aiccu.service

%changelog
* Tue Nov 29 2016 Zoltan Mezei <mezei.zoltan@gmail.com> - 2007.01.15-27
- Modify it to run on Centos 7

* Wed Jun 22 2016 Pavel Šimerda <psimerda@redhat.com> - 2007.01.15-26
- Resolves: #668767 - aiccu not running setupscript

* Fri Aug 28 2015 Pavel Šimerda <psimerda@redhat.com> - 2007.01.15-25
- Resolves: #1179274 - Utilize system-wide crypto-policies

* Thu Aug 27 2015 Pavel Šimerda <psimerda@redhat.com> - 2007.01.15-24
- Resolves: #1239365 - aiccu: FTBFS in rawhide

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 08 2014 Pavel Šimerda <psimerda@redhat.com> - 2007.01.15-22
- Related: #844607 - order also after time-sync.target

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 02 2014 Pavel Šimerda <psimerda@redhat.com> - 2007.01.15-19
- provide proper network/network-online dependencies

* Mon Jan 06 2014 Pavel Šimerda <psimerda@redhat.com> - 2007.01.15-18
- #850022 - use systemd-rpm macros

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 6 2012 Conrad Meyer <konrad@tylerc.org> - 2007.01.15-15
- Nix systemd restart as per discussion on #844607

* Tue Jul 31 2012 Conrad Meyer <konrad@tylerc.org> - 2007.01.15-14
- Adopt Eric Hopper's proposed changes (#844607)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Conrad Meyer <konrad@tylerc.org> - 2007.01.15-11
- Patch to syslog as DAEMON, not LOCAL7.

* Mon Jul 18 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2007.01.15-10
- Change service file to get not complains when /etc/sysconfig/aiccu is missing
- Change PID file in aiccu.conf to /run/aiccu.pid

* Wed Jul  6 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2007.01.15-9
- Implementing native systemd support (656886)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2007.01.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Oct 17 2008 Matt Domsch <mdomsch@fedoraproject.org> - 2007.01.15-5
- close file descriptors on exec (BZ#467381)

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> 2007.01.15-4 
- rebuild with new gnutls

* Fri Sep 21 2007 Matt Domsch <matt@domsch.com> 2007.01.15-3
- add LSB initscript header (BZ#246861)

* Wed Sep 19 2007 Matt Domsch <matt@domsch.com> 2007.01.15-2
- rebuild

* Wed Jan 31 2007 Matt Domsch <matt@domsch.com> 2007.01.15-1
- upgrade to latest upstream

* Sat Jan 13 2007 Matt Domsch <matt@domsch.com> 2007.01.07-2
- upstream respun their release with the same version number to fix AYIYA.

* Sun Jan 07 2007 Matt Domsch <matt@domsch.com> 2007.01.07-1
- upgrade to latest upstream 2007.01.07
  - license change to BSD 3-clause
  - Fixed up silly linux bug, adding LL address to tunnels but not to tun/taps.
  - local_ipv4_override option so one can use AICCU behind a NAT that
    has been configured correctly to do proto-41 forwarding. This is
    usually called a DMZ setup.

* Mon Oct 02 2006 Matt Domsch <matt@domsch.com> 2006.07.25-2
- rebuilt

* Sat Sep 23 2006 Matt Domsch <matt@domsch.com> 2006.07.25-1
- upgrade to latest upstream, drop all applied patches
- add BR gnutls-devel now used for obtaining tunnel info

* Sat Sep  2 2006 Matt Domsch <matt@domsch.com> 2005.01.31-5
- rebuild

* Wed Jun 28 2006 Matt Domsch <matt@domsch.com> 2005.01.31-4
- export CFLAGS properly, fix permissions on files for debuginfo

* Wed Jun 28 2006 Matt Domsch <matt@domsch.com> 2005.01.31-3
- cleanups per Fedora Extras review

* Sat Apr 22 2006 Matt Domsch <matt@domsch.com> 2005.01.31-2
- match Fedora Extras spec guidelines
- add postun condrestart
- add reload initscript arg to satisfy rpmlint

* Sun Aug 29 2004 Jeroen Massar <jeroen@sixxs.net> 2004.08.29
- Beta2 with TIC, 6in4, 6in4-heartbeat and AYIYA support

