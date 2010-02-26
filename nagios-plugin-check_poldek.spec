%define		commit	cbc143d
%define		plugin	check_poldek
Summary:	Nagios plugin to check PLD updates
Summary(pl.UTF_8):	Wtyczka Nagiosa sprawdzająca aktualizacje PLD
Name:		nagios-plugin-%{plugin}
Version:	0.1
Release:	0.1
License:	MIT
Group:		Networking
Source0:	http://github.com/pawelz/nagios-check_poldek/tarball/v0.1/%{name}.tar.gz
# Source0-md5:	3d3d829f19d31eeb3dba1037273d860f
URL:		http://github.com/pawelz/nagios-check_poldek
Requires:	nagios-common
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
Nagios plugin to check PLD updates.

%description -l pl.UTF-8
Wtyczka Nagiosa sprawdzająca aktualizacje PLD.

%prep
%setup -q -n pawelz-nagios-%{plugin}-%{commit}

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} -e $ARG1$ -w $ARG2$
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install -p %{plugin}.py $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(640,root,nagios) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
