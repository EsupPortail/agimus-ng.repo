%global AG_home /opt/%{name}
%global LDAP_SYS /etc/openldap/
Name:		agimus-ng-demo
Version:	1
Release:	1.ag%{?dist}
Summary:	Indicateur

Group:		System Environment/Daemons
License:	Apache2
URL:		https://www.esup-portail.org/wiki/display/AGIMUSNG
#Source0:	daily_batch.sh
#Source1:	%{name}.cron
Source2:	DB_CONFIG
Source3:	postfix.schema
Source4:	eduperson.schema
Source5:	supann.schema
Source6:	init_ldap.ldif
#BuildRequires:	
Requires:	openldap openldap-clients openldap-servers logstash logstash-contrib elasticsearch elasticsearch-plugin-kopf kibana

%description
Indicateur

%prep
#%setup -q


%build


%install

install -d %{buildroot}%{AG_home}/
install -d %{buildroot}%{_var}/lib/ldap/
install -d %{buildroot}%{_sysconfdir}/openldap/
install -d %{buildroot}%{_sysconfdir}/openldap/schema/
install -d %{buildroot}/tmp
install -m 755 %{SOURCE2} %{buildroot}%{_var}/lib/ldap/DB_CONFIG
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/openldap/schema/postfix.schema
install -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/openldap/schema/eduperson.schema
install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/openldap/schema/supann.schema
cp %{SOURCE6} %{buildroot}/tmp/init_ldap.ldif


%post
#start slapd
/usr/bin/systemctl start slapd

# Inject ldif
/usr/sbin/slapadd -l /tmp/%{SOURCE6} -b "dc=univ,dc=fr" -d 256

chown ldap:ldap -R /var/lib/ldap

#/sbin/service elasticsearch start


%files
#%dir %{buildroot}%{AG_home}/bin/
%{_sysconfdir}/openldap/schema
/tmp/init_ldap.ldif
%{_var}/lib/ldap/
#%{buildroot}%{_sysconfdir}/cron.d/%{name}.cron


%changelog
* Sat Jun 20 2015 ines.wallon@univ-lille1.fr 1
- Initial version
