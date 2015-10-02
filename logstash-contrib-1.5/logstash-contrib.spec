%global plugindir %{_datadir}/logstash
%global LS_home %{_libdir}/logstash

Name:		logstash-contrib
Version:	1.5.2
Release:	5.ag%{?dist}
Summary:	Contrib-logstash

Group:		System Environment/Daemons		
License:	ASL 2.0
URL:		http://logstash.net
Source0:	logstash-input-LDAPSearch-0.1.0.gem
Source1:	logstash-filter-translate-0.1.9.gem
Source2:	logstash-filter-cidr-0.1.6.gem
Source3:	logstash-filter-elasticsearch-0.1.6.gem

#BuildRequires:
Requires:	logstash
BuildArch:      noarch	
AutoReqProv: no

%description
A tool for managing events and logs.

%prep
#%setup -q

%postun
#rm -rf %{LS_home}/vendor

#%build
%pre
echo "Installation in progress. Please wait."
%post
#echo "Installation in progress. Please wait."
/usr/lib64/logstash/bin/plugin install /tmp/%{name}/logstash-input-LDAPSearch-0.1.0.gem
/usr/lib64/logstash/bin/plugin install /tmp/%{name}/logstash-filter-translate-0.1.9.gem
/usr/lib64/logstash/bin/plugin install /tmp/%{name}/logstash-filter-cidr-0.1.6.gem
/usr/lib64/logstash/bin/plugin install /tmp/%{name}/logstash-filter-elasticsearch-0.1.6.gem

rm -rf /tmp/%{name}/

%install
install -d  %{buildroot}/tmp/%{name}
cp -a %{SOURCE0} %{buildroot}/tmp/%{name}/
cp -a %{SOURCE1} %{buildroot}/tmp/%{name}/
cp -a %{SOURCE2} %{buildroot}/tmp/%{name}/
cp -a %{SOURCE3} %{buildroot}/tmp/%{name}/

%files
/tmp/%{name}/*
#%dir %{LS_home}
#%{LS_home}/*

%clean
rm -rf $RPM_BUILD_ROOT


%changelog

* Fri Sep 4 2015 ines.wallon@univ-lille1.fr 1.5-2
- Initial version

