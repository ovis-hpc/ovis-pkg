Name:		ovis-ldms-ui
Requires:	sosdb-ui
Version:	4.0.0
Release:	1%{?dist}
Summary:	This is web GUI for monitoring LDMS..

Group:		ovis-ui
License:	Dual GPL/BSD
URL:		http://www.opengridcomputing.com
Source0:	%{name}-%{version}.tar.gz

%define _prefix	/var/www/ovis_web_svcs

%description
LDMS Monitoring Web GUI and OVIS UI Infrastructure

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%defattr(-,apache,apache)
%{_prefix}

%changelog

