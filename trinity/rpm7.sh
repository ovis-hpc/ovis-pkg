#!/bin/bash
#
# README
#
# The aries libgpcd sampler needs the libgpcd library which is not
# a module installed on the system.
#
# The format ofthe option is as follows:
# --with-aries-libgpcd=LIBDIR,INCDIR for aries-mmr
#
ARIES_LIBGPCD=/home/totucke/install/opt/gpcd/lib,/home/totucke/install/opt/gpcd/include/gpcdlocal

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

WITH="$WITH_OVIS_LIB $WITH_GPCD_LIB"

function pkg_name() {
	case $1 in
	lib)
		echo -n "ovis-lib"
	;;
	ldms)
		echo -n "ovis-ldms"
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

LIST="lib ldms"
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
		--define "_with_aries_libgpcd $ARIES_LIBGPCD" \
		--define "_with_rca /opt/cray/rca/default" \
		--define "_with_krca /opt/cray/krca/default" \
		--define "_with_cray_hss_devel /opt/cray-hss-devel/default" \
		-ba $RPMBUILD/SPECS/$SPEC

	case $X in
	lib)
		RPM_PTN="ovis-lib"
	;;
	*)
		RPM_PTN=""
	;;
	esac
	if test -n "$RPM_PTN"; then
		# install ovis-lib and as build prerequisite of ldms
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
