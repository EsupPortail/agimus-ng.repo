%global K_home %{_datadir}/%{name}
%undefine _missing_build_ids_terminate_build
Name:		kibana
Version:	4.0.1
Release:	2.ag%{?dist}
Summary:	Kibana is an open source data visualization

Group:		System Environment/Daemons
License:	ASL 2.0
URL:		http://www.elasticsearch.org/
Source0:	https://download.elasticsearch.org/kibana/kibana/%{name}-%{version}-linux-x64.tar.gz
Source1:	kibana.initd

#BuildRequires:	
#Requires:	

BuildArch: x86_64

AutoReqProv: no

%description
Kibana is an open source data visualization platform that allows you to interact with your data through stunning, powerful graphics that can be combined into custom dashboards that help you share insights from your data far and wide. 

%prep
%setup -q -n kibana-4.0.1-linux-x64


%build


%install
install -d %{buildroot}%{K_home}/bin
install -d %{buildroot}%{K_home}/node
install -d %{buildroot}%{K_home}/plugins
install -d %{buildroot}%{K_home}/src
install -d %{buildroot}%{_sysconfdir}/init.d
install -d %{buildroot}%{_defaultdocdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/%{name}

cp -a bin/kibana  %{buildroot}%{K_home}/bin
cp -ra node/*  %{buildroot}%{K_home}/node
cp -ra plugins/*  %{buildroot}%{K_home}/plugins
cp -ra src/*  %{buildroot}%{K_home}/src
#Doc
cp -a  node/ChangeLog  %{buildroot}%{_defaultdocdir}/%{name}
cp -a  node/LICENSE  %{buildroot}%{_defaultdocdir}/%{name}
cp -a  node/README.md  %{buildroot}%{_defaultdocdir}/%{name}
cp -a  node/share/man/man1/node.1  %{buildroot}%{_defaultdocdir}/%{name}

#config
cp -a config/*  %{buildroot}%{_sysconfdir}/%{name}

#init script

install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}


%pre
# create elasticsearch group
if ! getent group kibana >/dev/null; then
  groupadd -r kibana
fi

# create logstash user
if ! getent passwd kibana >/dev/null; then
  useradd -r -g kibana -d %{K_home} -s /sbin/nologin -c "Kibana service user" kibana
fi

%post
/sbin/chkconfig --add %{name}
ln -s %{K_home}/bin/kibana /usr/bin/kibana


%preun

if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi



%files
%dir %{K_home}
%{_sysconfdir}/init.d/%{name}
%{K_home}/node/*
%{K_home}/bin/*
%{K_home}/plugins/*
%{K_home}/src/*
%{_defaultdocdir}/%{name}
%dir %{_sysconfdir}/%{name}
%attr(4755, %{name}, %{name}) %{_sysconfdir}/%{name}/%{name}.yml

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Mon Jun 22 2015 ines.wallon@univ-lille1.fr 4.0.1-1
- Initial version
