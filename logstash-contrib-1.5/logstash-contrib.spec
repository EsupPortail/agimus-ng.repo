
%global plugindir %{_datadir}/logstash
%global LS_home %{_libdir}/logstash

Name:		logstash-contrib
Version:	1.5.2
Release:	1.ag%{?dist}
Summary:	Contrib-logstash

Group:		System Environment/Daemons		
License:	ASL 2.0
URL:		http://logstash.net
#Source0:	http://download.elasticsearch.org/logstash/logstash/%{name}-%{version}.tar.gz
#Source1:	plugin_LDAP.tgz
#BuildRequires:
Requires:	logstash
BuildArch:      noarch	
AutoReqProv: no

%description
A tool for managing events and logs.

%prep
#%setup -q -a 1
#%setup -q -T -D -a 1

#%build

%post
/usr/lib64/logstash/bin/plugin install logstash-input-LDAPSearch
/usr/lib64/logstash/bin/plugin install logstash-filter-translate
/usr/lib64/logstash/bin/plugin install logstash-filter-cidr
/usr/lib64/logstash/bin/plugin install logstash-filter-elasticsearch

%install
#make install DESTDIR=%{buildroot}
#install -d  %{buildroot}%{plugindir}
#install -d %{buildroot}%{LS_home}/vendor/logstash
#cp -ar * %{buildroot}%{LS_home}/vendor/logstash

%files
#%dir %{LS_home}
#%{LS_home}/*

%clean
rm -rf $RPM_BUILD_ROOT


%changelog

* Fri Sep 4 2015 ines.wallon@univ-lille1.fr 1.5-2
- Initial version

