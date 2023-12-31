# Copyright (c) 2016 Open Grid Computing, Inc. All rights reserved.
# Copyright (c) 2016 Sandia Corporation. All rights reserved.
#
# Under the terms of Contract DE-AC04-94AL85000, there is a non-exclusive
# license for use of this work by or on behalf of the U.S. Government.
# Export of this program may require a license from the United States
# Government.
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
#      Neither the name of Sandia nor the names of any contributors may
#      be used to endorse or promote products derived from this software
#      without specific prior written permission.
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

Name: baler
Version: 4.1.1
Requires: sosdb >= %{version}
Obsoletes: baler < %{version}
Release: 1%{?dist}
Summary: Baler - a lossless, deterministic log processing tool
Group: Applications/System
License: GPLv2 or BSD
URL: https://www.opengridcomputing.com
Source0: %{name}-%{version}.tar.gz

%define _prefix /opt/ovis
%define _sysconfdir %{_prefix}/etc
%define _localstatedir %{_prefix}/var
%define _sharedstatedir %{_prefix}/var/lib
%define _systemdir /usr/lib/systemd/system

%description
Baler - a lossless, deterministic log processing tool.

%prep
%setup -q

%build
%configure \
	--enable-etc \
	--enable-swig \
	--enable-doc \
	--enable-doc-html \
	--enable-doc-man \
	--disable-rpath \
	--with-ovis-lib=%{_with_ovis_lib} \
	--with-sos=%{_with_sos} \
	CFLAGS="-g -O3"
# disable rpath when librool re-link
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=NO_RUNPATH_PLEASE|g' libtool
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
# remove unwanted .la files
/bin/rm -f %{buildroot}%{_libdir}/*.la

%clean
/bin/rm -rf %{buildroot}

# files for main package
%files
%{_bindir}
%{_libdir}
%{_prefix}/lib*/python*
%config %{_sysconfdir}/baler/*
%{_sysconfdir}/systemd
%exclude %{_bindir}/bclient

%posttrans
/bin/ln -fs %{_sysconfdir}/systemd/system/balerd.service %{_systemdir}/balerd.service
/usr/bin/systemctl daemon-reload

%post
/bin/rm -f /etc/profile.d/baler.sh
echo export BSTORE_PLUGIN_PATH=%{_libdir} > %{_sysconfdir}/baler/baler.sh
/bin/ln -fs %{_sysconfdir}/baler/baler.sh /etc/profile.d/baler.sh
/sbin/ldconfig

%preun
# /usr/bin/systemctl stop balerd.service

%postun
/bin/rm -f %{_systemdir}/balerd.service
/bin/rm -f /etc/profile.d/baler.sh
/usr/bin/systemctl daemon-reload
/sbin/ldconfig

# baler-devel package
%package devel
Summary: Development files for Baler
Group: Development/Libraries
%description devel
Development files for Baler
%files devel
%defattr(-,root,root)
%{_includedir}


# baler-bclient package
%package bclient
Summary: Baler interactive client for distributed baler
Group: Applications/System
Version: %{version}
Requires: baler >= %{version}, PyYAML >= 3.0, python-dateutil
%description bclient
`bclient` is a Baler interactive client with command-line interface for
distributed baler.
%files bclient
%defattr(-,root,root)
%{_bindir}/bclient

# baler-doc package
%package doc
Summary: Baler documentation
Group: Documentation
%description doc
Documentation for Baler package.
%files doc
%defattr(-,root,root)
%{_datadir}/doc
%{_datadir}/man


%changelog
