Name: ovis-ldms
Version: 4.3.4
Obsoletes: ovis-ldms < %{version}
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
		--enable-munge \
		--enable-swig \
		--enable-ldms-python \
                --enable-doc \
                --enable-doc-html \
                --enable-doc-man \
		--enable-lustre \
		--enable-jobinfo-slurm \
		--enable-spank-plugin \
		--enable-slurm-sampler \
		--with-slurm=/opt/slurm \
		--enable-ugni \
		--enable-kgnilnd \
		--enable-tsampler \
		--enable-cray_power_sampler \
		--enable-cray_system_sampler \
		--disable-gpcdlocal \
		--enable-aries-gpcdr \
		--enable-aries_mmr \
		--enable-aries_linkstatus \
		--enable-sos \
		--disable-dstat \
		--enable-kokkos \
		--enable-influx \
		--with-sos=%{_with_sos} \
		--with-ovis-lib=%{_with_ovis_lib} \
		--with-aries-libgpcd=%{_with_aries_libgpcd} \
		--with-rca=%{_with_rca} \
		--with-krca=%{_with_krca} \
		--with-cray-hss-devel=%{_with_cray_hss_devel} \
		--with-libpapi=%{_with_libpapi} \
		--with-libpfm=%{_with_libpapi} \
		--enable-syspapi-sampler \
		--enable-papi-sampler \
		CFLAGS="-g -O2"

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
%{_libdir}/libldmsd_stream.*
%{_libdir}/libldmsd_plugattr.*
%{_libdir}/libldmsd_request.*
%{_libdir}/libsampler_base.*
%{_libdir}/libldms_auth_*
%{_libdir}/ovis-ldms/ovis-ldms-configure-args
%{_libdir}/ovis-ldms/ovis-ldms-configure-env
%{_prefix}/lib*/python*
%{_libdir}/libcoll*
%{_libdir}/libovis_third*
%{_libdir}/libmmalloc*
%{_prefix}/lib*/python*/site-packages/ovis_ldms/*
%{_libdir}/libovis_auth*
%{_libdir}/libovis_ctrl*
%{_libdir}/libovis_event*
%{_libdir}/libovis_util*
%{_libdir}/libjson_util*
%{_libdir}/libzap.*
%{_libdir}/ovis-ldms/libzap_sock.*
%{_libdir}/ovis-ldms/libzap_ugni.*
%{_libdir}/ovis-ldms/ovis-auth.sh
%{_libdir}/ovis-lib-configvars.sh
%{_sysconfdir}/
%{_datadir}/doc/%{name}-%{version}/AUTHORS
%config %{_sysconfdir}/ldms/*
%config %{_sysconfdir}/systemd
%exclude %{_libdir}/ovis-ldms-configvars.sh
%exclude %{_libdir}/ovis-ldms/libstore_flatfile.*
%exclude %{_libdir}/ovis-ldms/libarray_example.*
%exclude %{_libdir}/ovis-ldms/libclock.*
%exclude %{_libdir}/ovis-ldms/libvariable.*
%exclude %{_libdir}/ovis-ldms/libstore_none.*
%exclude %{_sbindir}/json_test

%posttrans
/bin/rm -f %{_systemdir}/ldmsd.sampler.service
/bin/rm -f %{_systemdir}/ldmsd.aggregator.service
/bin/rm -f %{_systemdir}/ldmsd.kokkos.service
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.aggregator.service %{_systemdir}/ldmsd.aggregator.service
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.sampler.service %{_systemdir}/ldmsd.sampler.service
/bin/ln -fs %{_sysconfdir}/systemd/system/ldmsd.kokkos.service %{_systemdir}/ldmsd.kokkos.service
/bin/ln -fs %{_sysconfdir}/systemd/system/papi-sampler.service %{_systemdir}/papi-sampler.service
/bin/ln -fs %{_sysconfdir}/profile.d/set-ovis-variables.sh /etc/profile.d/set-ovis-variables.sh
/bin/ln -fs %{_sysconfdir}/ld.so.conf.d/ovis-ld-so.conf /etc/ld.so.conf.d/ovis-ld-so.conf
/usr/bin/systemctl daemon-reload

%post
/bin/rm -f /etc/profile.d/ovis.sh
echo PATH=%{_bindir}:%{_sbindir}:\$PATH > %{_sysconfdir}/ldms/ovis.sh
echo export LDMSD_PLUGIN_LIBPATH=%{_libdir}/ovis-ldms >> %{_sysconfdir}/ldms/ovis.sh
echo export ZAP_LIBPATH=%{_libdir}/ovis-ldms >> %{_sysconfdir}/ldms/ovis.sh
echo export PYTHONPATH=%{_prefix}/lib/python2.7/site-packages >> %{_sysconfdir}/ldms/ovis.sh
echo export LDMS_AUTH_FILE=%{_sysconfdir}/ldms/ldmsauth.conf >> %{_sysconfdir}/ldms/ovis.sh
/bin/ln -fs %{_sysconfdir}/ldms/ovis.sh /etc/profile.d/ovis.sh
/bin/rm -f %{_sysconfdir}/ldms/ldms-ldd.conf
/bin/rm -f /etc/ld.so.conf.d/ldms-ldd.conf
echo %{_libdir} > %{_sysconfdir}/ldms/ldms-ldd.conf
echo %{_libdir}/ovis-ldms >> %{_sysconfdir}/ldms/ldms-ldd.conf
echo %{_libdir}/ovis-ldms >> %{_sysconfdir}/ldms/ldms-ldd.conf
/bin/ln -fs %{_sysconfdir}/ldms/ldms-ldd.conf /etc/ld.so.conf.d/ldms-ldd.conf
/sbin/ldconfig

%preun
# /usr/bin/systemctl stop ldmsd.aggregator.service
# /usr/bin/systemctl stop ldmsd.sampler.service

%postun
/bin/rm -f %{_systemdir}/ldmsd.aggregator.service
/bin/rm -f %{_systemdir}/ldmsd.sampler.service
/bin/rm -f %{_systemdir}/ldmsd.kokkos.service
/bin/rm -f %{_systemdir}/papi-sampler.service
/bin/rm -f /etc/profile.d/set-ovis-variables.sh
/bin/rm -f /etc/ld.so.conf.d/ovis-ld-so.conf
/usr/bin/systemctl daemon-reload
/sbin/ldconfig

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

%package samplers
Summary: Sampler Plugins
Group: Applications/System
Requires: ovis-ldms >= %{version}
Version: %{version}
%description samplers
%{summary}
%files samplers
%defattr(-,root,root)
%{_libdir}/ovis-ldms/libgeneric_sampler.*
%{_libdir}/ovis-ldms/liblustre2_*
%{_libdir}/ovis-ldms/liblustre_*
%{_libdir}/ovis-ldms/libjobinfo.*
%{_libdir}/ovis-ldms/libjobinfo_slurm.*
%{_libdir}/ovis-ldms/libmeminfo.*
%{_libdir}/ovis-ldms/libprocdiskstats.*
%{_libdir}/ovis-ldms/libprocinterrupts.*
%{_libdir}/ovis-ldms/libprocnetdev.*
%{_libdir}/ovis-ldms/libprocnfs.*
%{_libdir}/ovis-ldms/libprocstat.*
%{_libdir}/ovis-ldms/libsynthetic.*
%{_libdir}/ovis-ldms/libvmstat.*
%{_libdir}/ovis-ldms/liball_example.*
%{_libdir}/ovis-ldms/libedac.*
%{_libdir}/ovis-ldms/liblnet_stats.*
%{_libdir}/ovis-ldms/libcray_dvs_sampler.*
%{_libdir}/ovis-ldms/libaries_linkstatus.*
%{_libdir}/ovis-ldms/libaries_mmr.*
%{_libdir}/ovis-ldms/libaries_nic_mmr.*
%{_libdir}/ovis-ldms/libaries_rtr_mmr.*
%{_libdir}/ovis-ldms/libcray_aries_r_sampler.*
%{_prefix}/etc/ldms/aries_mmr_set_configs
%{_libdir}/ovis-ldms/libcray_power_sampler.*
%{_libdir}/ovis-ldms/libtsampler.*
%{_libdir}/ovis-ldms/libtimer_base.*
%{_libdir}/ovis-ldms/libhfclock.*
%{_libdir}/ovis-ldms/libkgnilnd.*
%{_libdir}/ovis-ldms/libslurm_sampler.*
%{_libdir}/ovis-ldms/libslurm_notifier.*
%{_libdir}/ovis-ldms/libpapi_sampler.*
%{_libdir}/ovis-ldms/libsyspapi_sampler.*
%{_libdir}/ovis-ldms/libloadavg.*

#################
# store plugins #
#################

# ovis-ldms-store-csv-common
%package stores
Summary: Storage Plugins
Group: Applications/System
Requires: ovis-ldms >= %{version}
Version: %{version}
%description stores
%{summary}
%files stores
%defattr(-,root,root)
%{_libdir}/libldms_store_csv_common.*
%{_libdir}/ovis-ldms/libstore_csv.*
%{_libdir}/ovis-ldms/libstore_function_csv.*
%{_libdir}/ovis-ldms/libstore_sos.*
%{_libdir}/ovis-ldms/libkokkos_store.*
%{_libdir}/ovis-ldms/libstore_influx.*
%{_libdir}/ovis-ldms/libstore_papi.*
%{_libdir}/ovis-ldms/libstore_slurm.*

%package plugin-devel
Summary: Development files for LDMS plugins
Group: Development/Libraries
Requires: ovis-ldms >= %{version}
%description plugin-devel
Development files for LDMS plugins
%files plugin-devel
%defattr(-,root,root)
%{_includedir}/*

%changelog


