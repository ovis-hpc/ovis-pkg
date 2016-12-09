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
Version: 3.3.1
Release: 1%{?dist}
Obsoletes: SOS
Summary: Scalable Object Storage

%define _grp Application/Databases
Group: %{_grp}
License: GPLv2 or BSD
URL: http://www.ogc.us
Source0: %{name}-%{version}.tar.gz

Requires: libyaml >= 0.1.4
Prefix: %{_prefix}

%description
The Scalable Object Storage (SOS) is a high performance storage engine designed
to efficiently manage structured data on persistent media.

%prep
%setup -q


%build
%configure --enable-swig \
		--enable-etc \
		--enable-doc \
		--enable-doc-html \
		--enable-doc-man \
		--disable-rpath \
		CFLAGS='-g -O3'
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%clean
rm -rf %{buildroot}

# files for main package
%files
%{_bindir}/sos_*
%{_libdir}/libidx_*
%{_libdir}/libkey_*
%{_libdir}/libods.*
%{_libdir}/libsos.*
%{_prefix}/lib*/python*/site-packages/sosdb/


# sosdb-devel package
%package devel
Summary: Development files for sosdb
Group: %{_grp}
Obsoletes: SOS-devel
%description devel
PLACE HOLDER FOR sos-devel DESCRIPTION
%files devel
%defattr(-,root,root)
%{_includedir}/ods/
%{_includedir}/sos/


# sosdb-doc package
%package doc
Summary: sosdb documentation
Group: %{_grp}
Obsoletes: SOS-doc
%description doc
Documetnation for sosdb package.
%files doc
%defattr(-,root,root)
%{_datadir}/doc


# BWX packages, add `--enable-bwx` to configure option and change the condition
# to true here to build sosdb-bwx RPM.
%if 1==0

# sosdb-bwx package
%package bwx
Summary: bwx
Group: %{_grp}
Obsoletes: SOS-bwx
%description bwx
sosdb - Blue Water specific package.
%files bwx
%defattr(-,root,root)
%{_bindir}/bwx_*
%{_prefix}/lib*/python*/site-packages/bwx/

# sosdb-bwx-devel package
%package bwx-devel
Summary: bwx-devel
Group: %{_grp}
Obsoletes: SOS-bwx-devel
%description bwx-devel
Development files for sosdb-bwx package.
%files bwx-devel
%defattr(-,root,root)
%{_includedir}/bwx/

%endif # ENABLE_BWX_TRUE

%changelog
