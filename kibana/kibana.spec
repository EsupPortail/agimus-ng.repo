%global K_home %{_datadir}/%{name}

Name:		kibana
Version:	4.0.1
Release:	1.ag%{?dist}
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
%setup -q


%build


%install
install -d %{buildroot}%{K_home}/bin
install -d %{buildroot}%{K_home}/node
install -d %{buildroot}%{K_home}/plugins
install -d %{buildroot}%{K_home}/src


install -d %{buildroot}%{_sysconfdir}/%{name}

cp -a bin/kibana  %{buildroot}%{K_home}/bin
cp -ra node/*  %{buildroot}%{K_home}/node
cp -ra plugins/*  %{buildroot}%{K_home}/plugins
cp -ra src/*  %{buildroot}%{K_home}/src

#doc
cp -a  *.txt  %{buildroot}%{_defaultdocdir}/%{name}

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
%{K_home}/node/kibana

%dir %{K_home}/node
%dir %{K_home}/plugins
%dir %{K_home}/src
%dir %{_sysconfdir}/%{name}
%attr(4755, %{name}, %{name}) %{_sysconfdir}/%{name}/%{name}.yml

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

* Mon Jun 22 2015 antoine.wallon@univ-lille1.fr 4.0.1-1
- Initial version
