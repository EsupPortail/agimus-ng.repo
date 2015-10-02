%global AG_home /opt/agimus-ng
%global LDAP_SYS /etc/openldap/
Name:		agimus-ng-demo
Version:	1
Release:	11.ag%{?dist}
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
Source7:	daily_batch.sh
#Log
Source8:	25-moodle-access.log
Source9:	25-trace.log
Source10:	26-moodle-access.log
Source11:	26-trace.log
Source12:	27-moodle-access.log
Source13:	27-trace.log

#Log UL
Source14:	25-access-ent_UL.log
Source15:	25-serviceStats_UL.log
Source16:	26-access-ent_UL.log
Source17:       26-serviceStats_UL.log
Source18:       27-serviceStats_UL.log
Source19:       27-access-ent_UL.log



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
#install -d %{buildroot}%{AG_home}/demo
install -d %{buildroot}%{AG_home}/demo/logs/2015/09/25
install -d %{buildroot}%{AG_home}/demo/logs/2015/09/26
install -d %{buildroot}%{AG_home}/demo/logs/2015/09/27
install -d %{buildroot}%{_sysconfdir}/openldap/
install -d %{buildroot}%{_sysconfdir}/openldap/schema/
install -d %{buildroot}/tmp
install -d %{buildroot}%{_var}/lib/ldap/
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/openldap/
install -m 755 %{SOURCE2} %{buildroot}%{_var}/lib/ldap/DB_CONFIG
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/openldap/schema/postfix.schema
install -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/openldap/schema/eduperson.schema
install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/openldap/schema/supann.schema
install -m 755 %{SOURCE6} %{buildroot}%{AG_home}/demo/init_ldap.ldif
install -m 775 %{SOURCE7} %{buildroot}%{AG_home}/demo/daily_batch.sh

#Log d'example
cp -a %{SOURCE8} %{buildroot}%{AG_home}/demo/logs/2015/09/25/moodle-access.log
cp -a %{SOURCE9} %{buildroot}%{AG_home}/demo/logs/2015/09/25/trace.log
cp -a %{SOURCE10} %{buildroot}%{AG_home}/demo/logs/2015/09/26/moodle-access.log
cp -a %{SOURCE11} %{buildroot}%{AG_home}/demo/logs/2015/09/26/trace.log
cp -a %{SOURCE12} %{buildroot}%{AG_home}/demo/logs/2015/09/27/moodle-access.log
cp -a %{SOURCE13} %{buildroot}%{AG_home}/demo/logs/2015/09/27/trace.log
#Log UL
cp -a %{SOURCE14} %{buildroot}%{AG_home}/demo/logs/2015/09/25/access-ent_UL.log
cp -a %{SOURCE15} %{buildroot}%{AG_home}/demo/logs/2015/09/25/serviceStats_UL.log
cp -a %{SOURCE16} %{buildroot}%{AG_home}/demo/logs/2015/09/26/access-ent_UL.log
cp -a %{SOURCE17} %{buildroot}%{AG_home}/demo/logs/2015/09/26/26-serviceStats_UL.log
cp -a %{SOURCE18} %{buildroot}%{AG_home}/demo/logs/2015/09/27/serviceStats_UL.log
cp -a %{SOURCE19} %{buildroot}%{AG_home}/demo/logs/2015/09/27/access-ent_UL.log



%post

/usr/bin/systemctl stop slapd 

rm -rf /etc/openldap/slapd.d/*
rm -rf /var/lib/ldap/__db.00*
rm -rf /var/lib/ldap/*.bdb
rm -rf /var/lib/ldap/log.*
rm -rf /var/lib/ldap/alock

# Inject ldif
/usr/sbin/slapadd -l /opt/agimus-ng/demo/init_ldap.ldif -b "dc=univ,dc=fr"

chown ldap:ldap -R /var/lib/ldap


#/sbin/service elasticsearch start

%files
#%dir %{buildroot}%{AG_home}/bin/
%{_sysconfdir}/openldap/schema
%{_sysconfdir}/openldap/slapd.conf
%{_var}/lib/ldap/DB_CONFIG
/opt/agimus-ng/demo/*
#%{buildroot}%{_sysconfdir}/cron.d/%{name}.cron


%changelog
* Fri Sep 25 2015 ines.wallon@univ-lille1.fr 2
- Change BuildArch

* Sat Jun 20 2015 ines.wallon@univ-lille1.fr 1
- Initial version
