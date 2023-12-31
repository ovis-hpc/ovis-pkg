Name: ovis-ldms
Version: 3.4.4
Requires: ovis-lib-mmalloc >= %{version}, ovis-lib-ctrl >= %{version}, ovis-lib-coll >= %{version}
Release: 1%{?dist}
Summary: LDMS - Lighweight Distributed Metric Service

Group: Applications/System
License: GPLv2 or BSD
URL: https://www.opengridcomputing.com
Source0: %{name}-%{version}.tar.gz

%define _prefix /usr/local
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
		--enable-ldms-python \
                --enable-doc \
                --enable-doc-html \
                --enable-doc-man \
		--enable-sysclassib \
		--enable-lustre \
		--enable-sos \
		--disable-rdma \
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
#%exclude %{_sysconfdir}/init.d
#%exclude %{_sysconfdir}/ovis
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
Summary: LDMS Documentation
Group: Documentation
%description doc
Documentation for LDMS subsystem
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
Version: %{version}
%description sampler-generic
%{summary}
%files sampler-generic
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libgeneric_sampler.*

# ovis-ldms-sampler-lustre2
%package sampler-lustre2
Summary: Lustre2 LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
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
Version: %{version}
%description sampler-meminfo
%{summary}
%files sampler-meminfo
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libmeminfo.*

# ovis-ldms-sampler-procdiskstats
%package sampler-procdiskstats
Summary: Procdiskstats LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-procdiskstats
%{summary}
%files sampler-procdiskstats
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocdiskstats.*

# ovis-ldms-sampler-procinterrupts
%package sampler-procinterrupts
Summary: procinterrupts LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-procinterrupts
%{summary}
%files sampler-procinterrupts
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocinterrupts.*

# ovis-ldms-sampler-procnetdev
%package sampler-procnetdev
Summary: procnetdev LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-procnetdev
%{summary}
%files sampler-procnetdev
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocnetdev.*

# ovis-ldms-sampler-procnfs
%package sampler-procnfs
Summary: procnfs LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-procnfs
%{summary}
%files sampler-procnfs
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocnfs.*

# ovis-ldms-sampler-procsensors
%package sampler-procsensors
Summary: procsensors LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-procsensors
%{summary}
%files sampler-procsensors
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocsensors.*

# ovis-ldms-sampler-procstat
%package sampler-procstat
Summary: procstat LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-procstat
%{summary}
%files sampler-procstat
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libprocstat.*

# ovis-ldms-sampler-synthetic
%package sampler-synthetic
Summary: synthetic LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-synthetic
%{summary}
%files sampler-synthetic
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libsynthetic.*

# ovis-ldms-sampler-sysclassib
%package sampler-sysclassib
Summary: sysclassib LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-sysclassib
%{summary}
%files sampler-sysclassib
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libsysclassib.*

# ovis-ldms-sampler-vmstat
%package sampler-vmstat
Summary: vmstat LDMSD Vmstat Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-vmstat
%{summary}
%files sampler-vmstat
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libvmstat.*

# ovis-ldms-sampler-all
%package sampler-all
Summary: all LDMSD All Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-all
%{summary}
%files sampler-all
%defattr(-,root,root)
%{_libdir}/ovis-ldms/liball_example.*

# ovis-ldms-sampler-edac
%package sampler-edac
Summary: edac LDMSD EDAC Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-edac
%{summary}
%files sampler-edac
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libedac.*

# ovis-ldms-sampler-edac
%package sampler-lnet
Summary: lnet LDMSD LNET Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-lnet
%{summary}
%files sampler-lnet
%defattr(-,root,root)
%{_libdir}/ovis-ldms/liblnet_stats.*

#################
# store plugins #
#################

# ovis-ldms-store-csv-common
%package store-csv-common
Summary: CSV LDMSD Store Plugin Common Library
Group: Applications/System
Version: %{version}
%description store-csv-common
%{summary}
%files store-csv-common
%defattr(-,root,root)
%{_libdir}/libldms_store_csv_common.*

# ovis-ldms-store-csv
%package store-csv
Summary: CSV LDMSD Store Plugin
Group: Applications/System
Requires: ovis-ldms-store-csv-common >= %{version}
Version: %{version}
%description store-csv
%{summary}
%files store-csv
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libstore_csv.*

# ovis-ldms-store-function-csv
%package store-function-csv
Summary: LDMSD Function CSV Store Plugin
Group: Applications/System
Version: %{version}
Requires: ovis-ldms-store-csv-common >= %{version}
%description store-function-csv
%{summary}
%files store-function-csv
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libstore_function_csv.*

# ovis-ldms-store-sos
%package store-sos
Summary: LDMSD SOS Store Plugin
Group: Applications/System
Requires: sosdb >= %{version}
Version: %{version}
%description store-sos
%{summary}
%files store-sos
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libstore_sos.*

%changelog
