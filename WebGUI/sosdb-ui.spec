Name:		sosdb-ui
Version:	4.0.0
Release:	1%{?dist}
Summary:	SOS DB Web Interface

Group:		ovis-ui
License:	Dual BSD/GPL
URL:		http://www.opengridcomputing.com
Source0:	%{name}-%{version}.tar.gz

%define _prefix /var/www/ovis_web_svcs/
# BuildRequires:
# Requires:

%description
Django plugin that implements a Web interface to SOS object storage


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
#%{_prefix}/sosgui
#%{_prefix}/component/*
#%{_prefix}/container/*
#%{_prefix}/jobs/*
#%{_prefix}/objbrowser/*
#%{_prefix}/plot/*
#%{_prefix}/sos_db/*
#%{_prefix}/sosdb_auth/*
#%{_prefix}/manage.*
#%{_prefix}/README.md
#%{_prefix}/static
#%{_prefix}/templates


%changelog

