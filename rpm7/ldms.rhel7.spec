Name: ovis-ldms
Version: 3.3.2
Release: 1%{?dist}
Summary: LDMS - Lighweight Distributed Monitoring Service

%define _app_grp Applications/System
%define _dev_grp Development/System

Group: %{_app_grp}
License: GPLv2 or BSD
URL: http://www.ogc.us
Source0: %{name}-%{version}.tar.gz

Requires: ovis-lib-zap >= 1.3.0
Prefix: %{_prefix}
%define _sysconfdir %{_prefix}/etc
%define _localstatedir %{_prefix}/var
%define _sharedstatedir %{_prefix}/var/lib
%define _systemdir /usr/lib/systemd/system

%description
This package provides the LDMS commands and libraries.
* ldmsd: the LDMS daemon, which can run as sampler or aggregator (or both).
* ldms_ls: the tool to list metric information of an ldmsd.
* ldmsctl: the tool to control an ldmsd.


%prep
%setup -q


%build
%configure --enable-etc \
		--enable-swig \
		--enable-doc \
		--enable-doc-html \
		--enable-doc-man \
		--enable-test \
		--enable-ldms-python \
		--enable-rdma \
		--enable-sysclassib \
		--enable-sos \
		--with-ovis-lib=%{_ovis_src}/lib/build-rpm7/rpm7/BUILDROOT/opt/ovis \
		--with-sos=%{_ovis_src}/sos/build-rpm7/rpm7/BUILDROOT/opt/ovis \
		CFLAGS="-g -O3"
# NOTE: %{_ovis_src} macro is passed-in by rpm7.sh, the script calling rpmbuild
# with this spec file.
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# remove unwanted .la files
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

# files for main package
%files
%{_bindir}
%{_sbindir}
%{_libdir}
%{_prefix}/lib*/python*
%{_datadir}/doc/%{name}-%{version}/AUTHORS
%{_datadir}/doc/%{name}-%{version}/COPYING
%{_datadir}/doc/%{name}-%{version}/ChangeLog
%{_datadir}/doc/%{name}-%{version}/README
%config %{_sysconfdir}/ldms/*
%{_sysconfdir}/systemd
%exclude %{_sysconfdir}/init.d
%exclude %{_sysconfdir}/ovis

%posttrans
/sbin/ldconfig
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.aggregator.service %{_systemdir}/ldmsd.aggregator.service
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.sampler.service %{_systemdir}/ldmsd.sampler.service
/usr/bin/systemctl daemon-reload

%preun
/usr/bin/systemctl stop ldmsd.aggregator.service
/usr/bin/systemctl stop ldmsd.sampler.service

%postun
/bin/rm -f %{_systemdir}/ldmsd.aggregator.service
/bin/rm -f %{_systemdir}/ldmsd.sampler.service
/usr/bin/systemctl daemon-reload
/sbin/ldconfig


# ldms-devel package
%package devel
Summary: Development files for LDMS
Group: %{_grp}
%description devel
Development files for LDMS
%files devel
%defattr(-,root,root)
%{_includedir}


# ldms-doc package
%package doc
Summary: ldms documentation
Group: %{_grp}
%description doc
Documetnation for ldms project.
%files doc
%defattr(-,root,root)
%{_datadir}/doc
%{_datadir}/man


%changelog
