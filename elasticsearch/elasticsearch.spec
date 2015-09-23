
%global ES_home %{_datadir}/%{name}

Name:		elasticsearch	
Version:	1.4.2
Release:	2.ag%{?dist}
Summary:        Open source, flexible, distributed search and analytics engine
License:        ASL 2.0
URL:            http://www.elasticsearch.org/
Group:		System Environment/Daemons				
Source0:	https://download.elasticsearch.org/elasticsearch/elasticsearch/%{name}-%{version}.tar.gz
Source1:	%{name}.service
Source2:        %{name}.sysconfig
Source3:        %{name}.yml
Source4:        logging.yml

#BuildRequires:	
Requires: java-1.8.0-openjdk
Requires: jpackage-utils

Requires(post): chkconfig initscripts
Requires(preun): chkconfig initscripts
Requires(pre):  shadow-utils	

BuildArch:      noarch
# due to vendor/bundle
AutoReqProv: no
%description
Open source, flexible, distributed search and analytics engine for agimus


%prep
%setup -q


%build

%install
install -d %{buildroot}%{ES_home}/bin
install -d %{buildroot}%{ES_home}/lib
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}/tmp/%{name}
install -d %{buildroot}%{_defaultdocdir}/%{name}
install -d %{buildroot}%{_sysconfdir}/init.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_localstatedir}/run/%{name}/


cp -a bin/elasticsearch  %{buildroot}%{ES_home}/bin
cp -a bin/elasticsearch.in.sh  %{buildroot}%{ES_home}/bin
cp -a bin/plugin  %{buildroot}%{ES_home}/bin

cp -ar lib/*  %{buildroot}%{ES_home}/lib
cp -a  *.txt  %{buildroot}%{_defaultdocdir}/%{name}

install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/%{name}
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.yml
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/logging.yml


%pre
# create elasticsearch group
if ! getent group elasticsearch >/dev/null; then
  groupadd -r elasticsearch
fi

# create logstash user
if ! getent passwd elasticsearch >/dev/null; then
  useradd -r -g elasticsearch -d %{ES_home} -s /sbin/nologin -c "Elasticsearch service user" elasticsearch
fi

%post
/sbin/chkconfig --add %{name}
ln -s %{ES_home}/bin/elasticsearch /usr/bin/elasticsearch


%preun

if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%files

%dir %{ES_home}
%{ES_home}/lib/*
%{ES_home}/bin/elasticsearch
%{ES_home}/bin/elasticsearch.in.sh
%{ES_home}/bin/plugin



#Config
%{_sysconfdir}/sysconfig/%{name}
%attr(4755, %{name}, %{name}) %{_sysconfdir}/%{name}/%{name}.yml
%attr(4755, %{name}, %{name}) %{_sysconfdir}/%{name}/logging.yml

%dir %attr(4775, %{name}, %{name}) %{_localstatedir}/lib/%{name}
%dir %attr(4775, %{name}, %{name}) /tmp/%{name}

#doc
%dir %{_defaultdocdir}/%{name}
%{_defaultdocdir}/%{name}/*

#init file
%{_sysconfdir}/init.d/%{name}


%attr(4775, %{name}, %{name}) %{_localstatedir}/run/%{name}

#Log
%dir %attr(4755, %{name}, %{name}) %{_localstatedir}/log/%{name}
%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Mon Jun 22 2015 antoine.wallon@univ-lille1.fr 1.4-2
- Add symbolic link

* Thu Jun 18 2015 ines.wallon@univ-lille1.fr 1.4-2
- Initial version
