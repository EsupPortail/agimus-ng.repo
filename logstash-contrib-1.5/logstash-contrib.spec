%global plugindir %{_datadir}/logstash
%global LS_home %{_libdir}/logstash

Name:		logstash-contrib
Version:	1.5.2
Release:	2.ag%{?dist}
Summary:	Contrib-logstash

Group:		System Environment/Daemons		
License:	ASL 2.0
URL:		http://logstash.net
Source0:	vendor.tar.gz
#BuildRequires:
Requires:	logstash
BuildArch:      noarch	
AutoReqProv: no

%description
A tool for managing events and logs.

%prep
%setup -q -n vendor

%postun
rm -rf %{LS_home}/vendor
#%setup -q -T -D -a 1

#%build

%post

%install
#make install DESTDIR=%{buildroot}
#install -d  %{buildroot}%{plugindir}
#install -d %{buildroot}%{LS_home}/vendor/logstash
#cp -ar * %{buildroot}%{LS_home}/vendor/logstash
install -d %{buildroot}%{LS_home}/vendor
cp -r * %{buildroot}%{LS_home}/vendor
%files
%{LS_home}/vendor/*
#%dir %{LS_home}
#%{LS_home}/*

%clean
rm -rf $RPM_BUILD_ROOT


%changelog

* Fri Sep 4 2015 ines.wallon@univ-lille1.fr 1.5-2
- Initial version

