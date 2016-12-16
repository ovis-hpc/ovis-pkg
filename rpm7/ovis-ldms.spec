Name: ovis-ldms
Version: 3.3.0
Release: 1%{?dist}
Summary: LDMS - Lighweight Distributed Monitoring Service

Group: Applications/System
License: GPLv2 or BSD
URL: https://www.opengridcomputing.com
Source0: %{name}-%{version}.tar.gz

# Requires: ovis-lib-zap >= 1.3.0

BuildRequires: ovis-lib-auth-devel
BuildRequires: ovis-lib-coll-devel
BuildRequires: ovis-lib-ctrl-devel
BuildRequires: ovis-lib-mmalloc-devel
BuildRequires: ovis-lib-util-devel
BuildRequires: ovis-lib-zap-devel
BuildRequires: sosdb-devel
BuildRequires: swig
BuildRequires: python-devel
BuildRequires: libevent-devel
BuildRequires: libibmad-devel
BuildRequires: libibumad-devel
BuildRequires: libibverbs-devel

%define _prefix /opt/ovis
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
		--with-ovis-lib=%{_prefix} \
		--with-sos=%{_prefix} \
		CFLAGS="-g -O3"
# disable rpath when librool re-link
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=NO_RUNPATH_PLEASE|g' libtool
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
%{_libdir}/libldms.*
%{_prefix}/lib*/python*
%{_datadir}/doc/%{name}-%{version}/AUTHORS
%{_datadir}/doc/%{name}-%{version}/COPYING
%{_datadir}/doc/%{name}-%{version}/ChangeLog
%{_datadir}/doc/%{name}-%{version}/README
%config %{_sysconfdir}/ldms/*
%{_sysconfdir}/systemd
%exclude %{_sysconfdir}/init.d
%exclude %{_sysconfdir}/ovis
%exclude %{_libdir}/ovis-ldms-configvars.sh
%exclude %{_libdir}/ovis-ldms/libstore_flatfile.*
%exclude %{_libdir}/ovis-ldms/libarray_example.*
%exclude %{_libdir}/ovis-ldms/libclock.*

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


# ovis-ldms-devel package
%package devel
Summary: Development files for LDMS
Group: Development/Libraries
%description devel
Development files for LDMS
%files devel
%defattr(-,root,root)
%{_includedir}


# ovis-ldms-doc package
%package doc
Summary: ldms documentation
Group: Documentation
%description doc
Documetnation for ldms project.
%files doc
%defattr(-,root,root)
%{_datadir}/doc
%{_datadir}/man

###################
# sampler plugins #
###################

# ovis-ldms-sampler-generic
%package sampler-generic
Summary: Generic LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-generic
%{summary}
%files sampler-generic
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libgeneric_sampler.*

# ovis-ldms-sampler-lustre2
%package sampler-lustre2
Summary: Lustre2 LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-lustre2
%{summary}
%files sampler-lustre2
%defattr(-,root,root)
%{_libdir}/ovis-ldms/liblustre2_*
%{_libdir}/ovis-ldms/liblustre_*

# ovis-ldms-sampler-meminfo
%package sampler-meminfo
Summary: Meminfo LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-meminfo
%{summary}
%files sampler-meminfo
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libmeminfo.*

# ovis-ldms-sampler-procdiskstats
%package sampler-procdiskstats
Summary: Procdiskstats LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procdiskstats
%{summary}
%files sampler-procdiskstats
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocdiskstats.*

# ovis-ldms-sampler-procinterrupts
%package sampler-procinterrupts
Summary: procinterrupts LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procinterrupts
%{summary}
%files sampler-procinterrupts
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocinterrupts.*

# ovis-ldms-sampler-procnetdev
%package sampler-procnetdev
Summary: procnetdev LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procnetdev
%{summary}
%files sampler-procnetdev
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocnetdev.*

# ovis-ldms-sampler-procnfs
%package sampler-procnfs
Summary: procnfs LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procnfs
%{summary}
%files sampler-procnfs
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocnfs.*

# ovis-ldms-sampler-procsensors
%package sampler-procsensors
Summary: procsensors LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procsensors
%{summary}
%files sampler-procsensors
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocsensors.*

# ovis-ldms-sampler-procstat
%package sampler-procstat
Summary: procstat LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procstat
%{summary}
%files sampler-procstat
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocstat.*

# ovis-ldms-sampler-procstatutil
%package sampler-procstatutil
Summary: procstatutil LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-procstatutil
%{summary}
%files sampler-procstatutil
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocstatutil.*

# ovis-ldms-sampler-synthetic
%package sampler-synthetic
Summary: synthetic LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-synthetic
%{summary}
%files sampler-synthetic
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libsynthetic.*

# ovis-ldms-sampler-sysclassib
%package sampler-sysclassib
Summary: sysclassib LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-sysclassib
%{summary}
%files sampler-sysclassib
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libsysclassib.*

# ovis-ldms-sampler-vmstat
%package sampler-vmstat
Summary: vmstat LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-vmstat
%{summary}
%files sampler-vmstat
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libvmstat.*

# ovis-ldms-sampler-lnet_stats
%package sampler-lnet_stats
Summary: Lustre Network Statistics LDMSD Sampler Plugin
Group: Applications/System
Version: 3.3.0
%description sampler-lnet_stats
%{summary}
%files sampler-lnet_stats
%defattr(-,root,root)
%{_libdir}/ovis-ldms/liblnet_stats.*


#################
# store plugins #
#################

# ovis-ldms-store-csv
%package store-csv
Summary: CSV LDMSD Store Plugin
Group: Applications/System
Version: 3.3.0
%description store-csv
%{summary}
%files store-csv
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libstore_csv.*

# ovis-ldms-store-function-csv
%package store-function-csv
Summary: Function CSV LDMSD Store Plugin
Group: Applications/System
Version: 3.3.0
%description store-function-csv
%{summary}
%files store-function-csv
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libstore_function_csv.*

# ovis-ldms-store-sos
%package store-sos
Summary: CSV LDMSD Store Plugin
Group: Applications/System
Version: 3.3.0
%description store-sos
%{summary}
%files store-sos
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libstore_sos.*

%changelog
