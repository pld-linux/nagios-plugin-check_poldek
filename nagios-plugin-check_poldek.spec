%define		plugin	check_poldek
Summary:	Nagios plugin to check updates of poldek based systems
Summary(pl.UTF-8):	Wtyczka Nagiosa sprawdzająca aktualizacje systemów używających poldka
Name:		nagios-plugin-%{plugin}
Version:	0.8
Release:	4
License:	MIT
Group:		Networking
Source0:	http://github.com/pawelz/nagios-check_poldek/tarball/v%{version}/%{plugin}-%{version}.tgz
# Source0-md5:	0ee3a35c35c2f2ec16c001ff16cac0e2
Source1:	%{plugin}.cfg
Patch0:		defaults.patch
URL:		http://github.com/pawelz/nagios-check_poldek
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.685
Requires:	grep
Requires:	nagios-common
Requires:	poldek >= 0.30-1.rc3
Requires:	python-modules
Requires:	sed >= 4.0
Conflicts:	nagios-nrpe < 2.15-5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		nrpeddir	/etc/nagios/nrpe.d
%define		plugindir	%{_prefix}/lib/nagios/plugins
%define		cachedir	/var/cache/check_poldek

%description
Nagios plugin to check updates of poldek based systems.

%description -l pl.UTF-8
Wtyczka Nagiosa sprawdzająca aktualizacje systemów używających poldka.

%prep
%setup -qc
mv */* .
%patch -P0 -p1

%{__sed} -i -e "s,@repos@,['%{pld_release}']," %{plugin}.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{nrpeddir},%{plugindir},%{cachedir}}
install -p %{plugin}.py $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg
touch $RPM_BUILD_ROOT%{nrpeddir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- nagios-nrpe
%nagios_nrpe -a %{plugin} -f %{_sysconfdir}/%{plugin}.cfg

%triggerun -- nagios-nrpe
%nagios_nrpe -d %{plugin} -f %{_sysconfdir}/%{plugin}.cfg

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%ghost %{nrpeddir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
%dir %attr(775,root,nagios) %{cachedir}
