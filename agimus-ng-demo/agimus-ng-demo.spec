%global AG_home /opt/%{name}
%global LDAP_SYS /etc/openldap/
Name:		agimus-ng-demo
Version:	1
Release:	6.ag%{?dist}
Summary:	Indicateur

Group:		System Environment/Daemons
License:	Apache2
URL:		https://www.esup-portail.org/wiki/display/AGIMUSNG
#Source0:	daily_batch.sh
Source1:	slapd.conf
Source2:	DB_CONFIG
Source3:	postfix.schema
Source4:	eduperson.schema
Source5:	supann.schema
Source6:	init_ldap.ldif
#BuildRequires:	
Requires:	openldap openldap-clients openldap-servers logstash logstash-contrib elasticsearch elasticsearch-plugin-kopf kibana
BuildArch:      noarch
%description
Indicateur

%prep
#%setup -q


%build


%install

install -d %{buildroot}%{AG_home}/
#install -d %{buildroot}%{_var}/lib/ldap/
install -d %{buildroot}%{_sysconfdir}/openldap/
install -d %{buildroot}%{_sysconfdir}/openldap/schema/
install -d %{buildroot}/tmp
install -d %{buildroot}%{_var}/lib/ldap/
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/openldap/
install -m 755 %{SOURCE2} %{buildroot}%{_var}/lib/ldap/DB_CONFIG
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/openldap/schema/postfix.schema
install -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/openldap/schema/eduperson.schema
install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/openldap/schema/supann.schema
install -m 755 %{SOURCE6} %{buildroot}/tmp/init_ldap.ldif


%post

/usr/bin/systemctl stop slapd 

rm -rf /etc/openldap/slapd.d/*
rm -rf /var/lib/ldap/__db.00*
rm -rf /var/lib/ldap/*.bdb
rm -rf /var/lib/ldap/log.*
rm -rf /var/lib/ldap/alock

# Inject ldif
/usr/sbin/slapadd -l /tmp/init_ldap.ldif -b "dc=univ,dc=fr"

rm -rf /tmp/init_ldap.ldif
chown ldap:ldap -R /var/lib/ldap


#/sbin/service elasticsearch start

%files
#%dir %{buildroot}%{AG_home}/bin/
%{_sysconfdir}/openldap/schema
%{_sysconfdir}/openldap/slapd.conf
/tmp/init_ldap.ldif
%{_var}/lib/ldap/DB_CONFIG
#%{buildroot}%{_sysconfdir}/cron.d/%{name}.cron


%changelog
* Fri Sep 25 2015 ines.wallon@univ-lille1.fr 2
- Change BuildArch

* Sat Jun 20 2015 ines.wallon@univ-lille1.fr 1
- Initial version
