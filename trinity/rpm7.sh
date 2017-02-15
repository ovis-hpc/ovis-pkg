#!/bin/bash
#
# README
#
# This script is meant to be run on a dedicated RPM Build machine. The script
# will remove existing ovis-lib-*, sosdb-*, ovis-ldms-*, and baler-*
# installation before building. The script also call `yum` several times to
# install dependencies needed for the build. The following is the sequence of
# routines executed by this script:
#
# 0. yum remove 'ovis-lib-*' 'sosdb-*' 'ovis-ldms-*' 'baler-*'
# 1. ovis-lib
#    - make ovis-lib dist tarball
#    - rpmbuild ovis-lib
#    - yum install ovis-lib-* (needed to build ovis-ldms and baler)
#
# 2. sosdb
#    - make sosdb dist tarball
#    - rpmbuild sosdb
#    - yum install sosdb (needed to build ovis-ldms and baler)
#
# 3. ovis-ldms
#    - make ovis-ldms dist tarball
#    - rpmbuild ovis-ldms
#
# 4. build baler
#    - make baler dist tarball
#    - rpmbuild baler
#
# 5. The RPMS can be found in $PWD/rpmbuild/RPMS
# 6. The SRPMS can be found in $PWD/rpmbuild/SRPMS

OVIS_SRC=$(dirname $PWD)/ovis

CFLAGS='-g -O3'

# Exit immediately if a command failed
set -e

ARCH=$(uname -m)

RPMBUILD=$PWD/rpmbuild
mkdir -p $RPMBUILD/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

TMP_ROOT=$PWD/tmproot
TMP_ROOT_PREFIX=$TMP_ROOT/opt/ovis
mkdir -p $TMP_ROOT_PREFIX

WITH_OVIS_LIB="--with-ovis-lib=$TMP_ROOT_PREFIX"
WITH_SOS="--with-sos=$TMP_ROOT_PREFIX"

WITH="$WITH_OVIS_LIB $WITH_SOS"

function pkg_name() {
	case $1 in
	lib)
		echo -n "ovis-lib"
	;;
	sos)
		echo -n "sosdb"
	;;
	ldms)
		echo -n "ovis-ldms"
	;;
	baler)
		echo -n "baler"
	;;
	*)
		exit -1
	;;
	esac
}

function spec_name() {
	echo -n $(pkg_name $1).spec
}

function yum_group_check_install() {
	GRP="$1"
	X=$(yum grouplist installed "$GRP" 2>/dev/null | wc -l)
	test "$X" -gt 0 || sudo yum groupinstall "$GRP"
}

function yum_check_install() {
	for _X in $@; do
		yum list installed $_X >/dev/null 2>&1 || sudo yum install $_X
	done
}

# sudo yum remove 'ovis-lib-*' 'sosdb-*' 'ovis-ldms-*' 'baler-*'
# yum_group_check_install "Development Tools"
# yum_check_install \
#	autoconf \
#	automake \
#	swig \
#	python-devel \
#	libtool \
#	libevent-devel \
#	libibverbs-devel \
#	libibmad-devel \
#	libibumad-devel \
#	librdmacm-devel \
#	openssl-devel \
#	libyaml-devel

LIST="lib sos ldms baler"
for X in $LIST; do
	echo "----------------------------------"
	echo "$X"
	echo "----------------------------------"
	set -x; # enable command echo

	# First, generate the source tarball
	pushd ../ovis/$X
	./autogen.sh
	BUILD_DIR=$PWD/build-rpm7
	mkdir -p $BUILD_DIR
	pushd $BUILD_DIR
	rm -rf * # Making sure that the build is clean
	../configure $WITH # doesn't need other options here as this is for
			   # `make dist` only. For the enable/disable
			   # options for each package, please see configure
			   # options in their spec files.
	make dist

	cp *.tar.gz $RPMBUILD/SOURCES
	popd # $BUILD_DIR
	popd # ../ovis/$X

	SPEC=$(spec_name $X)
	cp $SPEC $RPMBUILD/SPECS
	rpmbuild --define "_topdir $RPMBUILD" \
		--define "_with_ovis_lib $TMP_ROOT_PREFIX" \
		--define "_with_sos $TMP_ROOT_PREFIX" \
		-ba $RPMBUILD/SPECS/$SPEC

	case $X in
	lib)
		RPM_PTN="ovis-lib"
	;;
	sos)
		RPM_PTN="sosdb"
	;;
	*)
		RPM_PTN=""
	;;
	esac
	if test -n "$RPM_PTN"; then
		# install ovis-lib and sosdb as build prerequisite of ldms
		# and baler
		# sudo yum install -y $RPMBUILD/RPMS/$ARCH/${RPM_PTN}-*.rpm
		pushd $TMP_ROOT
		for R in $RPMBUILD/RPMS/$ARCH/${RPM_PTN}-*.rpm; do
			rpm2cpio $R | cpio -dium
		done
		popd
	fi

	set +x; # disable command echo so that it won't print the "for ..." command
	echo "----- DONE -----"
done

echo "FINISH: Please find RPMS and SRPMS in ./rpmbuild/RPMS and ./rpmbuild/SRPMS respectively"
