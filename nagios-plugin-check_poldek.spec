%define		plugin	check_poldek
Summary:	Nagios plugin to check updates of poldek based systems
Summary(pl.UTF-8):	Wtyczka Nagiosa sprawdzająca aktualizacje systemów używających poldka
Name:		nagios-plugin-%{plugin}
Version:	0.5
Release:	1
License:	MIT
Group:		Networking
Source0:	http://github.com/pawelz/nagios-check_poldek/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f1b67d7640f1c1558e6e99838b66a331
URL:		http://github.com/pawelz/nagios-check_poldek
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

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} --cache %{cachedir} -c $ARG1$ -w $ARG2$
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir},%{cachedir}}
install -p %{plugin}.py $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

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
