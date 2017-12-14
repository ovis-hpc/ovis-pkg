# Set topdir to be builddir/rpm
# note this is intentionally ignored by rpmbuild. must use
# commandline syntax in makefile.am to get this effect.
#%-define _topdir %(echo $PWD)/rpm
#%-define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

# Main package
Summary: OVIS common libraries
Name: ovis-lib
Version: 4.0.0
Obsoletes: ovis-lib < %{version}
Release: 1%{?dist}
License: GPLv2 or BSD
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: %{name}-%{version}.tar.gz

# BuildRequires: swig
BuildRequires: python-devel
# BuildRequires: libibverbs-devel
# BuildRequires: librdmacm-devel
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
                --enable-doc-man \
                --enable-rdma \
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
rm -f $RPM_BUILD_ROOT%{_bindir}/test_notification
rm -f $RPM_BUILD_ROOT%{_bindir}/test_util

%clean
rm -rf $RPM_BUILD_ROOT

# coll
%package coll
Summary: OVIS API for managing collections of objects
Obsoletes: ovis-lib-coll < %{version}
Group: Development/Libraries
%description coll
A library of API for managing collections of objects that includes
the following:
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
Obsoletes: ovis-lib-coll-devel < %{version}
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
Obsoletes: ovis-lib-mmalloc < %{version}
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
Obsoletes: ovis-lib-mmalloc-devel < %{version}
Group: Development/Libraries
%description mmalloc-devel
Development files for ovis-mmalloc library
%files mmalloc-devel
%defattr(-,root,root)
%{_includedir}/mmalloc/

# auth
%package auth
Summary: OVIS authentication library
Obsoletes: ovis-lib-auth < %{version}
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
Obsoletes: ovis-lib-auth-devel < %{version}
Summary: Development files for ovis-lib-auth library
Group: Development/Libraries
%description auth-devel
Development files for ovis-lib-auth library
%files auth-devel
%defattr(-,root,root)
%{_includedir}/ovis_auth/

# ctrl
%package ctrl
Requires: ovis-lib-util >= %{version}
Summary: OVIS CLI control library
Group: Development/Libraries
Obsoletes: ovis-lib-ctrl < %{version}
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
Obsoletes: ovis-lib-ctrl-devel < %{version}
%description ctrl-devel
Development files for ovis-lib-ctrl library
%files ctrl-devel
%defattr(-,root,root)
%{_includedir}/ovis_ctrl/

# event
%package event
Summary: OVIS event library
Group: Development/Libraries
Obsoletes: ovis-lib-event < %{version}
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
Obsoletes: ovis-lib-event-devel < %{version}
%description event-devel
Development files for ovis-lib-event library
%files event-devel
%defattr(-,root,root)
%{_includedir}/ovis_event/

# util
%package util
Summary: OVIS utility library
Group: Development/Libraries
Obsoletes: ovis-lib-util < %{version}
%description util
OVIS utility library
%files util
%defattr(-,root,root)
%{_libdir}/libovis_util*
%{_libdir}/libovis_util.so.0
%{_libdir}/libjson_parser*

%post util
/sbin/ldconfig
%postun util
/sbin/ldconfig

# util-devel
%package util-devel
Summary: Development files for ovis-lib-util library
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-util-devel < %{version}
%description util-devel
Development files for ovis-lib-util library
%files util-devel
%defattr(-,root,root)
%{_includedir}/ovis_util/
%{_includedir}/json_parser/json.h

# zap
%package zap
Summary: Transport Independent User-mode RDMA API
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-zap < %{version}
%description zap
Zap is a Transport Independent User-mode RDMA API
%files zap
%defattr(-,root,root)
%{_libdir}/libzap.*
# %{_sbindir}/zap_test*

%post zap
/sbin/ldconfig
%postun zap
/sbin/ldconfig

# zap-devel
%package zap-devel
Summary: Development files for ovis-lib-zap library
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-zap-devel < %{version}
Requires: ovis-lib-zap >= %{version}
%description zap-devel
Development files for ovis-lib-zap library
%files zap-devel
%defattr(-,root,root)
%{_includedir}/zap/

# zap-sock
%package zap-sock
Summary: Socket transport implementation for Zap
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-zap-sock < %{version}
Requires: ovis-lib-zap >= %{version}, ovis-lib-coll >= %{version}, libevent >= 2.0.21
%description zap-sock
Socket transport implementation for Zap
%files zap-sock
%defattr(-,root,root)
%{_libdir}/ovis-lib/libzap_sock.*

# zap-rdma
%package zap-rdma
Summary: RDMA transport implementation for Zap
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-zap-rdma < %{version}
Requires: ovis-lib-zap >= %{version}, ovis-lib-coll >= %{version}, libevent >= 2.0.21
%description zap-rdma
RDMA transport implementation for Zap
%files zap-rdma
%defattr(-,root,root)
%{_libdir}/ovis-lib/libzap_rdma.*

# python
%package python
Summary: Python API for ovis_lib services
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-python < %{version}
%description python
Python API for ovis_lib services
%files python
%defattr(-,root,root)
%{_prefix}/lib*/python*/site-packages/ovis_lib/*

%package misc
Summary: Miscellaneous files in the ovis-lib project.
Group: Development/Libraries
Version: %{version}
Obsoletes: ovis-lib-misc < %{version}
%description misc
Miscellaneous files in the ovis-lib project.
%files misc
%{_libdir}/ovis-lib-configvars.sh
%{_includedir}/ovis-lib-config.h
%{_bindir}/lib-pedigree
%{_sysconfdir}/
%{_prefix}/share/doc/ovis-lib-*/COPYING
%{_prefix}/share/doc/ovis-lib-*/README
%{_prefix}/share/doc/ovis-lib-*/ChangeLog
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
