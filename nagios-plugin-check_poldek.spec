%define		plugin	check_poldek
Summary:	Nagios plugin to check updates of poldek based systems
Summary(pl.UTF-8):	Wtyczka Nagiosa sprawdzająca aktualizacje systemów używających poldka
Name:		nagios-plugin-%{plugin}
Version:	0.6
Release:	1
License:	MIT
Group:		Networking
#Source0:	http://github.com/pawelz/nagios-check_poldek/tarball/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/glensc/nagios-check_poldek/tarball/master/%{plugin}-%{version}.tgz
# Source0-md5:	fba5849a184ec310e018dd2ead225647
Source1:	%{plugin}.cfg
Patch0:		defaults.patch
URL:		http://github.com/pawelz/nagios-check_poldek
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.552
Requires:	grep
Requires:	nagios-common
Requires:	poldek
Requires:	python-modules
Requires:	sed
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins
%define		cachedir	/var/cache/check_poldek

%description
Nagios plugin to check updates of poldek based systems.

%description -l pl.UTF-8
Wtyczka Nagiosa sprawdzająca aktualizacje systemów używających poldka.

%prep
%setup -qc
mv */* .
%patch0 -p1

%{__sed} -i -e "s,@repos@,['%{pld_release}']," %{plugin}.py

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir},%{cachedir}}
install -p %{plugin}.py $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- nagios-nrpe
%nagios_nrpe -a %{plugin} -f %{_sysconfdir}/%{plugin}.cfg

%triggerun -- nagios-nrpe
%nagios_nrpe -d %{plugin} -f %{_sysconfdir}/%{plugin}.cfg

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
%dir %attr(775,root,nagios) %{cachedir}
