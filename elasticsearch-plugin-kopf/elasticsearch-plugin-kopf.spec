%global ES_home %{_datadir}/elasticsearch
Name:		elasticsearch-plugin-kopf
Version:	1.5.4
Release:	1.ag%{?dist}
Summary:	kopf is a simple web administration tool for ElasticSearch

Group:		System Environment/Daemons
License:	MIT
URL:		https://github.com/lmenezes/elasticsearch-kopf/
Source0:	https://github.com/lmenezes/elasticsearch-kopf/archive/master.zip

#BuildRequires:	
Requires:	elasticsearch
BuildArch:      noarch
# due to vendor/bundle
AutoReqProv: no

%description
kopf is a simple web administration tool for ElasticSearch written in JavaScript + AngularJS + jQuery + Twitter bootstrap.
It offers an easy way of performing common tasks on an elasticsearch cluster. Not every single API is covered by this plugin, but it does offer a REST client which allows you to explore the full potential of the ElasticSearch API.

%prep
%setup -q -n elasticsearch-kopf-master


%build


%install
install -d %{buildroot}%{ES_home}/plugins/kopf/_site
cp -ar * %{buildroot}%{ES_home}/plugins/kopf/_site 

%files
#%dir
%{ES_home}/plugins/kopf/_site/*

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Jun 20 2015 antoine.wallon@univ-lille1.fr 1.5-4
- Initial version
