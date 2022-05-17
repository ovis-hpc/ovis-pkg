# Copyright (c) 2015-2016 Open Grid Computing, Inc. All rights reserved.
#
# This software is available to you under a choice of one of two
# licenses.  You may choose to be licensed under the terms of the GNU
# General Public License (GPL) Version 2, available from the file
# COPYING in the main directory of this source tree, or the BSD-type
# license below:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#      Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#      Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#      Neither the name of Open Grid Computing nor the names of any
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#      Modified source versions must be plainly marked as such, and
#      must not be misrepresented as being the original software.
#
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Name: sosdb
Version: 5.1.1
Obsoletes: sosdb < %{version}
Release: 1%{?dist}
Summary: Scalable Object Storage

Group: Application/Databases
License: GPLv2 or BSD
URL: https://www.opengridcomputing.com
Source0: %{name}-%{version}.tar.gz

BuildRequires: python-devel

%define _prefix /opt/ovis

%description
The Scalable Object Storage (SOS) is a high performance storage engine designed
to efficiently manage structured data on persistent media.

%prep
%setup -q

%build
%configure \
    --enable-python \
    --enable-doc \
    --enable-doc-html \
    --enable-doc-man \
    COMMIT_ID=%{_commit_id} \
    CFLAGS="-g -O3 -fPIC"

# disable rpath when librool re-link
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=NO_RUNPATH_PLEASE|g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

# files for main package
%files
%defattr(-,root,root)
%{_bindir}/ods_dump
%{_bindir}/sos_*
%{_bindir}/sos-db
%{_bindir}/sos-import-csv
%{_bindir}/sos-monitor
%{_bindir}/sos-part
%{_bindir}/sos-schema
%{_bindir}/dsosql
%{_bindir}/dsosd
%{_bindir}/rpcgen
%{_libdir}/libidx_*
%{_libdir}/libkey_*
%{_libdir}/libods.*
%{_libdir}/libsos.*
%{_libdir}/libdsos.*
%{_libdir}/libsos_json.*
%{_libdir}/sos-configvars.sh
%{_libdir}/libtirpc.*
%{_prefix}/lib*/python*/site-packages/sosdb/
%{_includedir}/ods/
%{_includedir}/sos/
%{_includedir}/dsos.h
%exclude %{_includedir}/tirpc
%exclude /etc/bindresvport.blacklist
%exclude /etc/netconfig
%exclude %{_libdir}/pkgconfig/libtirpc.pc

# sosdb-doc package
%package doc
Summary: sosdb documentation
Obsoletes: sosdb-doc < %{version}
Group: Documentation
Obsoletes: SOS-doc
%description doc
Documetnation for sosdb package.
%files doc
%defattr(-,root,root)
%{_datadir}/doc
%{_datadir}/man

