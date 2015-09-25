
#%global bindir %{_bindir}
#%global confdir %{_sysconfdir}/%{name}
%global homedir %{_sharedstatedir}/%{name}
#%global jarpath %{_javadir}
#%global lockfile %{_localstatedir}/lock/subsys/%{name}
%global logdir %{_localstatedir}/log/%{name}
%global piddir %{_localstatedir}/run/%{name}
%global plugindir %{_datadir}/%{name}
#%global sysconfigdir %{_sysconfdir}/sysconfig

%global LS_home %{_libdir}/%{name}

Name:           logstash
Version:        1.5.2
Release:        2.ag%{?dist}
Summary:        A tool for managing events and logs

Group:          System Environment/Daemons
License:        ASL 2.0
URL:            http://logstash.net
Source0:        https://download.elasticsearch.org/logstash/logstash/%{name}-%{version}.tar.gz
Source1:        logstash.wrapper
Source2:        logstash.logrotate
Source3:        logstash.init
Source4:        logstash.env
Source5:        logstash.service
# BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# due to vendor/bundle
AutoReqProv: no

BuildRequires: systemd

Requires: systemd
Requires: java-1.8.0-openjdk
Requires: jpackage-utils
# Requires:       jruby # maybe later shift to version provided by distribution

# Requires(post): chkconfig initscripts
# Requires(pre):  chkconfig initscripts
# Requires(pre):  shadow-utils

%description
A tool for managing events and logs.

%prep
%setup -q

%build

%install

# Environment file
install -d %{buildroot}%{_sysconfdir}/logstash
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}.env

%{__sed} -i \
  -e "s|@@@NAME@@@|%{name}|g" \
  -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}|g" \
  -e "s|@@@LOGDIR@@@|%{logdir}|g" \
  -e "s|@@@PLUGINDIR@@@|%{plugindir}|g" \
  -e "s|@@@JAVA_IO_TMPDIR@@@|%{piddir}/java_io|g" \
  %{buildroot}%{_sysconfdir}/%{name}.env


# Systemd unit
install -d %{buildroot}/%{_unitdir}
install -m 755 %{SOURCE5} %{buildroot}/%{_unitdir}/

%{__sed} -i \
  -e "s|@@@LS_HOME@@@|%{LS_home}|g" \
  -e "s|@@@CONFDIR@@@|%{_sysconfdir}/%{name}.d|g" \
  -e "s|@@@USRSHARE@@@|%{_datarootdir}|g" \
  -e "s|@@@ENVFILE@@@|%{_sysconfdir}/%{name}.env|g" \
  %{buildroot}/%{_unitdir}/logstash.service

# Config dir
install -d %{buildroot}%{_sysconfdir}/%{name}.d

# Plugin dir
install -d  %{buildroot}%{plugindir}/inputs
install -d  %{buildroot}%{plugindir}/filters
install -d  %{buildroot}%{plugindir}/outputs
install -d  %{buildroot}%{plugindir}/patterns  # see if it really usable


# Logs
install -d  %{buildroot}%{_localstatedir}/log/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Misc
install -d %{buildroot}%{piddir}
install -d %{buildroot}%{piddir}/java_io


# Executables
# See header, we cannot place executables into the correct place
#  In fact thist script can be replaced with custom, but it doesn't solve other
#  path inconsistencies (.
#
# install -d %{buildroot}%{_bindir}
# install -m 755 bin/logstash %{buildroot}%{_bindir}/logstash
# install -m 755 bin/logstash.lib.sh %{buildroot}%{_bindir}/logstash.lib.sh

# Libs (and almost anything to run daemon)

install -d %{buildroot}%{LS_home}/lib
#install -d %{buildroot}%{LS_home}/vendor
install -d %{buildroot}%{LS_home}/bin

cp -ar lib/*  %{buildroot}%{LS_home}/lib/
#cp -ar vendor/*  %{buildroot}%{LS_home}/vendor/
cp -ar bin/*  %{buildroot}%{LS_home}/bin/

# Create Home directory
#   See https://github.com/lfrancke/logstash-rpm/issues/5
install -d  %{buildroot}%{homedir}

%pre
# create logstash group
if ! getent group logstash >/dev/null; then
  groupadd -r logstash
fi

# create logstash user
if ! getent passwd logstash >/dev/null; then
  useradd -r -g logstash -d %{homedir} -s /sbin/nologin -c "Logstash service user" logstash
fi

%post
# read new unit
systemctl daemon-reload

%preun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
# Systemd service
%{_unitdir}/*

# Executables
# %{_bindir}/*

# Libs
%dir %{LS_home}
%{LS_home}/lib/*
%{LS_home}/bin/*

# Config
%{_sysconfdir}/%{name}.env
%dir  %{_sysconfdir}/%{name}.d/


# Plugin dir
%dir %{plugindir}/inputs
%dir %{plugindir}/filters
%dir %{plugindir}/outputs
%dir %{plugindir}/patterns

# Logrotate
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%defattr(-,%{name},%{name},-)
%dir %{logdir}/
%dir %{piddir}/

# Home directory
%dir %{homedir}/

%changelog

* Wed Jun 17 2015 ines.wallon@univ-lille1.fr 1.5-2
- Initial version

