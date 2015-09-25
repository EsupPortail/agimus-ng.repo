Name:		agimus-repo
Version:	1
Release:	2.ag%{?dist}
Summary:	Indicateur

Group:		System Environment/Daemons
License:	Apache2
URL:		https://www.esup-portail.org/wiki/display/AGIMUSNG
#Source0:	daily_batch.sh
Source1:	agimus.repo
#BuildRequires:	
BuildArch:      noarch
%description
Repository installation

%prep


%build


%install

install -d %{buildroot}%{_sysconfdir}/yum.repos.d/
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/

%post


%files
%{_sysconfdir}/yum.repos.d/agimus.repo


%changelog
* Fri Sep 25 2015 ines.wallon@univ-lille1.fr 1
- Initial Version
