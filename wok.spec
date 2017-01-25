Name:		wok
Version:	2.3.1
Release:	0%{?dist}
Summary:	Wok - Webserver Originated from Kimchi
BuildRoot:	%{_topdir}/BUILD/%{name}-%{version}-%{release}
BuildArch:	noarch
Group:		System Environment/Base
License:	LGPL/ASL2
Source0:	%{name}-%{version}.tar.gz
Patch1:	wok-2.3.1-pidof-friendly.patch
Requires:	gettext
Requires:	python-cherrypy >= 3.2.0
Requires:	python-cheetah
Requires:	m2crypto
Requires:	PyPAM
Requires:	python-jsonschema >= 1.3.0
Requires:	python-lxml
Requires:	nginx
Requires:	python-ldap
Requires:	python-psutil >= 0.6.0
Requires:	fontawesome-fonts
Requires:	open-sans-fonts
Requires:	logrotate
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  firewalld
BuildRequires:	gettext-devel
BuildRequires:	libxslt
BuildRequires:	openssl
BuildRequires:	python-lxml

%global with_systemd 1

%if 0%{?with_systemd}
Requires:	systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%if 0%{?with_systemd}
BuildRequires: systemd-units
%endif

%description
Wok is Webserver Originated from Kimchi.


%prep
%setup -q
%patch1 -p1 -b .pidof


%build
./autogen.sh --system
%configure
make


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%if 0%{?rhel} == 6
# Install the upstart script
install -Dm 0755 contrib/wokd-upstart.conf.fedora %{buildroot}/etc/init/wokd.conf
%endif
%if 0%{?rhel} == 5
# Install the SysV init scripts
install -Dm 0755 contrib/wokd.sysvinit %{buildroot}%{_initrddir}/wokd
%endif

%post
if [ $1 -eq 1 ] ; then
    /bin/systemctl enable wokd.service >/dev/null 2>&1 || :
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun

if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable wokd.service > /dev/null 2>&1 || :
    /bin/systemctl stop wokd.service > /dev/null 2>&1 || :
fi

exit 0


%postun
if [ "$1" -ge 1 ] ; then
    /bin/systemctl try-restart wokd.service >/dev/null 2>&1 || :
fi
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(-,root,root)
%{_bindir}/wokd
%{python_sitelib}/wok/*.py*
%{python_sitelib}/wok/control/*.py*
%{python_sitelib}/wok/model/*.py*
%{python_sitelib}/wok/xmlutils/*.py*
%{python_sitelib}/wok/API.json
%{python_sitelib}/wok/plugins/*.py*
%{python_sitelib}/wok/
%{_prefix}/share/locale/*/LC_MESSAGES/wok.mo
%{_datadir}/wok/ui/
%{_datadir}/wok
%{_sysconfdir}/nginx/conf.d/wok.conf.in
%{_sysconfdir}/wok/wok.conf
%{_sysconfdir}/wok/
%{_sysconfdir}/logrotate.d/wokd
%{_mandir}/man8/wokd.8.gz

%if 0%{?with_systemd}
%{_sysconfdir}/nginx/conf.d/wok.conf
%{_sharedstatedir}/wok/
%{_localstatedir}/log/wok/*
%{_localstatedir}/log/wok/
%{_unitdir}/wokd.service
%{_prefix}/lib/firewalld/services/wokd.xml
%endif
%if 0%{?rhel} == 6
/etc/init/wokd.conf
%endif
%if 0%{?rhel} == 5
%{_initrddir}/wokd
%endif

%changelog
* Tue Jan 24 2017 eGloo <developer@egloo.ca> 2.3.1
- First build

* Fri Jun 19 2015 Lucio Correia <luciojhc@linux.vnet.ibm.com> 2.0
- Rename to wokd
- Remove kimchi specifics

* Thu Feb 26 2015 Frédéric Bonnard <frediz@linux.vnet.ibm.com> 1.4.0
- Add man page for kimchid

* Tue Feb 11 2014 Crístian Viana <vianac@linux.vnet.ibm.com> 1.1.0
- Add help pages and XSLT dependency

* Tue Jul 16 2013 Adam Litke <agl@us.ibm.com> 0.1.0-1
- Adapted for autotools build

* Thu Apr 04 2013 Aline Manera <alinefm@br.ibm.com> 0.0-1
- First build
