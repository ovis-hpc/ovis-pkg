# Set topdir to be builddir/rpm
# note this is intentionally ignored by rpmbuild. must use
# commandline syntax in makefile.am to get this effect.
#%-define _topdir %(echo $PWD)/rpm
#%-define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0
%define zap_version 1.3.1

# Main package
Summary: OVIS Common Libraries
Name: ovis-lib
Version: 3.3.0
Release: 1%{?dist}
License: GPLv2 or BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: %{name}-%{version}.tar.gz

BuildRequires: swig
BuildRequires: python-devel
BuildRequires: libibverbs-devel
BuildRequires: librdmacm-devel
BuildRequires: libevent-devel
BuildRequires: openssl-devel

Url: https://www.opengridcomputing.com/
%define _prefix /opt/ovis
%define _sysconfdir %{_prefix}/etc
%define _localstatedir %{_prefix}/var
%define _sharedstatedir %{_prefix}/var/lib

%description
This package provides common OVIS libraries.

%prep
%setup -q

%build
%configure --enable-swig \
		--enable-etc \
		--enable-doc \
		--enable-doc-html \
		--enable-doc-man \
		--enable-test \
		--enable-zaptest \
		--enable-rdma \
		--enable-etc \
		--disable-rpath \
		CFLAGS='-g -O3'
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_bindir}/test_big_dstring
rm -f $RPM_BUILD_ROOT%{_bindir}/test_dstring
rm -f $RPM_BUILD_ROOT%{_bindir}/test_rman
rm -f $RPM_BUILD_ROOT%{_bindir}/test_olog

%clean
rm -rf $RPM_BUILD_ROOT

# coll
%package coll
Summary: OVIS collection data structure library
Group: Development/Libraries
%description coll
This is a library of collection data structure commonly used in OVIS project.
This library contains an implementation of the following data structure:
- Red-Black Tree
- String Hash Table
%files coll
%defattr(-,root,root)
%{_libdir}/libcoll*
%{_libdir}/libovis_third*

%post coll
/sbin/ldconfig
%postun coll
/sbin/ldconfig

# coll-devel
%package coll-devel
Summary: Development files for ovis-lib-coll library
Group: Development/Libraries
%description coll-devel
Development files for ovis-coll library.
%files coll-devel
%defattr(-,root,root)
%{_includedir}/coll/

# mmalloc
%package mmalloc
Summary: OVIS memory allocation library
Group: Development/Libraries
%description mmalloc
OVIS memory allocation library
%files mmalloc
%defattr(-,root,root)
%{_libdir}/libmmalloc*

%post mmalloc
/sbin/ldconfig
%postun mmalloc
/sbin/ldconfig

# mmalloc-devel
%package mmalloc-devel
Summary: Development files for ovis-lib-mmalloc library
Group: Development/Libraries
%description mmalloc-devel
Development files for ovis-mmalloc library
%files mmalloc-devel
%defattr(-,root,root)
%{_includedir}/mmalloc/

# auth
%package auth
Summary: OVIS authentication library
Group: Development/Libraries
%description auth
OVIS authentication library
%files auth
%defattr(-,root,root)
%{_libdir}/libovis_auth*
%{_libdir}/ovis-lib/ovis-auth.sh

%post auth
/sbin/ldconfig
%postun auth
/sbin/ldconfig

# auth-devel
%package auth-devel
Summary: Development files for ovis-lib-auth library
Group: Development/Libraries
%description auth-devel
Development files for ovis-lib-auth library
%files auth-devel
%defattr(-,root,root)
%{_includedir}/ovis_auth/

# ctrl
%package ctrl
Summary: OVIS CLI control library
Group: Development/Libraries
%description ctrl
OVIS CLI control utility library
%files ctrl
%defattr(-,root,root)
%{_libdir}/libovis_ctrl*

%post ctrl
/sbin/ldconfig
%postun ctrl
/sbin/ldconfig

# ctrl-devel
%package ctrl-devel
Summary: Development files for ovis-lib-ctrl library
Group: Development/Libraries
%description ctrl-devel
Development files for ovis-lib-ctrl library
%files ctrl-devel
%defattr(-,root,root)
%{_includedir}/ovis_ctrl/

# event
%package event
Summary: OVIS event library
Group: Development/Libraries
%description event
OVIS event library
%files event
%defattr(-,root,root)
%{_libdir}/libovis_event*

%post event
/sbin/ldconfig
%postun event
/sbin/ldconfig

# event-devel
%package event-devel
Summary: Development files for ovis-lib-event library
Group: Development/Libraries
%description event-devel
Development files for ovis-lib-event library
%files event-devel
%defattr(-,root,root)
%{_includedir}/ovis_event/

# util
%package util
Summary: OVIS utility library
Group: Development/Libraries
%description util
OVIS utility library
%files util
%defattr(-,root,root)
%{_libdir}/libovis_util*

%post util
/sbin/ldconfig
%postun util
/sbin/ldconfig

# util-devel
%package util-devel
Summary: Development files for ovis-lib-util library
Group: Development/Libraries
%description util-devel
Development files for ovis-lib-util library
%files util-devel
%defattr(-,root,root)
%{_includedir}/ovis_util/

# zap
%package zap
Summary: asynchronous transport abstraction library
Group: Development/Libraries
Version: %{zap_version}
%description zap
Zap is an asynchronous transport abstraction library for various OVIS
applications. It eases the network programming part in application development,
so that the application doesn't have to pay much attention to the real
underlying transports (e.g. socket, rdma (Infiniband or iWarp), and uGNI).
%files zap
%defattr(-,root,root)
%{_libdir}/libzap.*
%{_sbindir}/zap_test*

%post zap
/sbin/ldconfig
%postun zap
/sbin/ldconfig

# zap-devel
%package zap-devel
Summary: Development files for ovis-lib-zap library
Group: Development/Libraries
Version: %{zap_version}
Requires: ovis-lib-zap >= 1.3.0
%description zap-devel
Development files for ovis-lib-zap library
%files zap-devel
%defattr(-,root,root)
%{_includedir}/zap/

# zap-sock
%package zap-sock
Summary: socket transport implementation for zap
Group: Development/Libraries
Version: %{zap_version}
Requires: ovis-lib-zap >= 1.3.0, ovis-lib-coll, libevent >= 2.0.21
%description zap-sock
socket transport implementation for zap
%files zap-sock
%defattr(-,root,root)
%{_libdir}/ovis-lib/libzap_sock.*

%package zap-rdma
Summary: RDMA (Infiniband and iWarp) transport implementation for zap
Group: Development/Libraries
Version: %{zap_version}
Requires: ovis-lib-zap >= 1.3.0, librdmacm >= 1.0.19, libibverbs >= 1.1.8
%description zap-rdma
RDMA (Infiniband and iWarp) transport implementation for zap
%files zap-rdma
%defattr(-,root,root)
%{_libdir}/ovis-lib/libzap_rdma.*

# python
%package python
Summary: Python interface for OVIS libraries
Group: Development/Libraries
%description python
Python interface for OVIS libraries
%files python
%{_prefix}/lib*/python*/site-packages/ovis_lib/

# ovis-lib-doc package
%package doc
Summary: ovis-lib documentation
Group: Documentation
%description doc
Documetnation for ovis-lib package.
%files doc
%defattr(-,root,root)
%{_datadir}/doc


%package misc
Summary: Miscellaneous file in ovis-lib project.
Group: Development/Libraries
%description misc
Miscellaneous file in ovis-lib project.
%files misc
%{_libdir}/ovis-lib-configvars.sh
%{_includedir}/ovis-lib-config.h
%{_bindir}/lib-pedigree
%{_sysconfdir}/
# These are the files that we don't care
%exclude %{_includedir}/ovis-test/

%posttrans misc
/bin/ln -fs %{_sysconfdir}/profile.d/set-ovis-variables.sh /etc/profile.d/set-ovis-variables.sh
/bin/ln -fs %{_sysconfdir}/ld.so.conf.d/ovis-ld-so.conf /etc/ld.so.conf.d/ovis-ld-so.conf
/sbin/ldconfig
%postun misc
/bin/rm -f /etc/profile.d/set-ovis-variables.sh
/bin/rm -f /etc/ld.so.conf.d/ovis-ld-so.conf
/sbin/ldconfig

%changelog
