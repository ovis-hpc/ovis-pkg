Name:		ovis-baler-ui
Version:	4.0.0
Release:	1%{?dist}
Summary:	This is web GUI for monitoring Baler.

Group:		ovis-ui
License:	Dual GPL/BSD
URL:		http://www.opengridcomputing.com
Source0:	%{name}-%{version}.tar.gz

%define _prefix /var/www/ovis_web_svcs/

%description
Baler Monitoring Web GUI


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,apache,apache)
%{_prefix}

%changelog

