Name: ovis-ldms
Version: 4.0.0
Requires: ovis-lib-mmalloc >= %{version}, ovis-lib-ctrl >= %{version}, ovis-lib-coll >= %{version}
Release: 1%{?dist}
Summary: LDMS - Lighweight Distributed Metric Service

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
                --enable-ugni \
		--enable-kgnilnd \
                --enable-doc \
                --enable-doc-html \
                --enable-doc-man \
		--enable-sysclassib \
		--enable-lustre \
		--enable-tsampler \
		--enable-cray_power_sampler \
		--enable-cray_system_sampler \
		--disable-gpcdlocal \
		--enable-aries-gpcdr \
		--enable-aries_mmr \
		--enable-aries_linkstatus \
		--enable-jobinfo \
		--enable-jobinfo-slurm \
		--enable-sos \
		--enable-rdma \
		--disable-mmap \
		--disable-readline \
		--with-slurm=%{_with_slurm} \
		--with-sos=%{_with_sos} \
		--with-ovis-lib=%{_with_ovis_lib} \
		--with-aries-libgpcd=%{_with_aries_libgpcd} \
		--with-rca=%{_with_rca} \
		--with-krca=%{_with_krca} \
		--with-cray-hss-devel=%{_with_cray_hss_devel} \
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
%{_bindir}/envldms.sh
%{_bindir}/ldms_ban.sh
%{_bindir}/ldms-meminfo.sh
%{_bindir}/ldms-pedigree
%{_bindir}/ldms_plugins_list.sh
%{_bindir}/ldms-py-edac_test.sh
%{_bindir}/ldms-py-fptrans_test.sh
%{_bindir}/ldms-py-subset_test.sh
%{_bindir}/ldms-py-syslog.sh
%{_bindir}/ldms-py-rename.sh
%{_bindir}/ldms-py-varset.sh
%{_sbindir}
%{_libdir}/libldms.*
%{_datadir}/doc/%{name}-%{version}/AUTHORS
%{_datadir}/doc/%{name}-%{version}/COPYING
%{_datadir}/doc/%{name}-%{version}/ChangeLog
%{_datadir}/doc/%{name}-%{version}/README
%config %{_sysconfdir}/ldms/*
%{_sysconfdir}/systemd
%exclude %{_libdir}/ovis-ldms-configvars.sh
%exclude %{_libdir}/ovis-ldms/libstore_flatfile.*
%exclude %{_libdir}/ovis-ldms/libarray_example.*
%exclude %{_libdir}/ovis-ldms/libclock.*
%exclude %{_libdir}/ovis-ldms/libvariable.*

%posttrans
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.aggregator.service %{_systemdir}/ldmsd.aggregator.service
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.sampler.service %{_systemdir}/ldmsd.sampler.service
/usr/bin/systemctl daemon-reload

%post
/bin/rm -f /etc/profile.d/ovis.sh
echo PATH=%{_bindir}:%{_sbindir}:\$PATH > %{_sysconfdir}/ldms/ovis.sh
echo export LDMSD_PLUGIN_LIBPATH=%{_libdir}/ovis-ldms >> %{_sysconfdir}/ldms/ovis.sh
echo export ZAP_LIBPATH=%{_libdir}/ovis-lib >> %{_sysconfdir}/ldms/ovis.sh
echo export PYTHONPATH=%{_prefix}/lib/python2.7/site-packages >> %{_sysconfdir}/ldms/ovis.sh
/bin/ln -fs %{_sysconfdir}/ldms/ovis.sh /etc/profile.d/ovis.sh
/bin/rm -f %{_sysconfdir}/ldms/ldms-ldd.conf
/bin/rm -f %{_sysconfdir}/ldms/ldms-ldd.conf
echo %{_libdir} > %{_sysconfdir}/ldms/ldms-ldd.conf
echo %{_libdir}/ovis-ldms >> %{_sysconfdir}/ldms/ldms-ldd.conf
echo %{_libdir}/ovis-lib >> %{_sysconfdir}/ldms/ldms-ldd.conf
/bin/ln -fs %{_sysconfdir}/ldms/ldms-ldd.conf /etc/ld.so.conf.d/ldms-ldd.conf
/sbin/ldconfig

%preun
/usr/bin/systemctl stop ldmsd.aggregator.service
/usr/bin/systemctl stop ldmsd.sampler.service

%postun
/bin/rm -f %{_systemdir}/ldmsd.aggregator.service
/bin/rm -f %{_systemdir}/ldmsd.sampler.service
/usr/bin/systemctl daemon-reload
/sbin/ldconfig

# ovis-ldms-python package
%package python
Summary: Python tools and interfaces package
Group: Development/Libraries
%description python
Python tools and evelopment interfaces
%files python
%defattr(-,root,root)
%{_bindir}/ldmsd_controller
%{_prefix}/lib*/python*

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

# ovis-ldms-sampler-jobinfo
%package sampler-jobinfo
Summary: Job Information Sampler
Group: Applications/System
Version: %{version}
%description sampler-jobinfo
%{summary}
%files sampler-jobinfo
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libjobinfo.*
%{_libdir}/ovis-ldms/libjobinfo_slurm.*

# ovis-ldms-sampler-tsampler
%package sampler-tsampler
Summary: High Frequency Sampler Plugins
Group: Applications/System
Version: %{version}
%description sampler-tsampler
%{summary}
%files sampler-tsampler
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libtsampler.*
%{_libdir}/ovis-ldms/libhfclock.*
%{_libdir}/ovis-ldms/libtimer_base.*

# ovis-ldms-sampler-cray-dvs
%package sampler-cray-dvs
Summary: Cray DVS Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-cray-dvs
%{summary}
%files sampler-cray-dvs
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libcray_dvs_sampler.*

# ovis-ldms-sampler-cray-aries
%package sampler-cray-aries
Summary: Cray Aries Sampler Plugins
Group: Applications/System
Version: %{version}
%description sampler-cray-aries
%{summary}
%files sampler-cray-aries
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libaries_linkstatus.*
%{_libdir}/ovis-ldms/libaries_mmr.*
%{_libdir}/ovis-ldms/libaries_nic_mmr.*
%{_libdir}/ovis-ldms/libaries_rtr_mmr.*
%{_libdir}/ovis-ldms/libcray_aries_r_sampler.*
%{_prefix}/etc/ldms/aries_mmr_set_configs

# ovis-ldms-sampler-cray-power
%package sampler-cray-power
Summary: Cray Power Sampler Plugins
Group: Applications/System
Version: %{version}
Requires: ovis-ldms-sampler-tsampler >= %{version}
%description sampler-cray-power
%{summary}
%files sampler-cray-power
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libcray_power_sampler.*

# ovis-ldms-sampler-kgnilnd
%package sampler-kgnilnd
Summary: Cray KGNI LND LDMS Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-kgnilnd
%{summary}
%files sampler-kgnilnd
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libkgnilnd.*

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

# ovis-ldms-sampler-lnet_stats
%package sampler-lnet_stats
Summary: Lustre Network Statistics LDMSD Sampler Plugin
Group: Applications/System
Version: %{version}
%description sampler-lnet_stats
%{summary}
%files sampler-lnet_stats
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
