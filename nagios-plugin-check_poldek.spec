# TODO
# - add support for specifying repo names via -n, --sn
%define		plugin	check_poldek
Summary:	Nagios plugin to check updates of poldek based systems
Summary(pl.UTF_8):	Wtyczka Nagiosa sprawdzająca aktualizacje systemów używających poldka
Name:		nagios-plugin-%{plugin}
Version:	0.2
Release:	1
License:	MIT
Group:		Networking
Source0:	http://github.com/pawelz/nagios-check_poldek/tarball/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9cd3838772a47c1941a8ae7f16bdc925
URL:		http://github.com/pawelz/nagios-check_poldek
BuildRequires:	rpmbuild(macros) >= 1.552
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

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
	command_line    %{plugindir}/%{plugin} --cache /var/cache/check_poldek -e $ARG1$ -w $ARG2$
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir},/var/cache/check_poldek}
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
%dir %attr(775,root,nagios) /var/cache/check_poldek
