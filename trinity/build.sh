#!/bin/bash
#
# README
#
# This shell file creates RPM intended for the Cray CLE7
# environment.
#
# The source is expected to be in ../ovis, and ../sos
#
# Be aware that your modules environment will affect
# where and if the code installed by your RPM will run.
#
# module unload PrgEnv-intel
# module unload PrgEnv-gnu
# module load PrgEnv-gnu
# module load python/2.7-anaconda-4.1.1
# module unload perftools-base
# module load papi
LIBPAPI=/opt/cray/pe/papi/5.6.0.6
ARIES_LIBGPCD=/opt/cray/gni/default/lib64,/opt/cray/gni/default/include/gpcd
PLATFORM=Voltrino
OVIS_SRC=$(dirname $PWD)/ovis

CFLAGS='-g -O3'

# Exit immediately if a command failed
set -e

ARCH=$(uname -m)

RPMBUILD=$PWD/rpmbuild
rm -rf $RPMBUILD
mkdir -p $RPMBUILD/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

TMP_ROOT=$PWD/tmproot
rm -rf $TMP_ROOT

TMP_ROOT_PREFIX=$TMP_ROOT/opt/ovis
mkdir -p $TMP_ROOT_PREFIX

WITH_OVIS_LIB="--with-ovis-lib=$TMP_ROOT_PREFIX"
WITH_SLURM="--with-slurm=/opt/slurm"

WITH="$WITH_OVIS_LIB $WITH_SOS $WITH_SLURM"

function pkg_name() {
    case $1 in
        ovis)
	    echo -n "ovis"
	    ;;
	sos)
	    echo -n "sosdb"
	    ;;
	*)
	    exit -1
	    ;;
    esac
}

function spec_name() {
    echo -n $(pkg_name $1).spec
}

LIST="sos ovis"
for X in $LIST; do
	echo "----------------------------------"
	echo "$X"
	echo "----------------------------------"
	set -x; # enable command echo

	# First, generate the source tarball
	pushd ../$X
	COMMIT_ID="$(git rev-parse HEAD 3>/dev/null)"

	./autogen.sh
	BUILD_DIR=$PWD/build-${PLATFORM}
	mkdir -p $BUILD_DIR
	pushd $BUILD_DIR
	rm -rf * # Making sure that the build is clean
	../configure COMMIT_ID=$COMMIT_ID $WITH
	make dist

	cp *.tar.gz $RPMBUILD/SOURCES
	popd # $BUILD_DIR
	popd # ../ovis/$X
done

LIST="sos ovis"
for X in $LIST; do
	echo "----------------------------------"
	echo "$X"
	echo "----------------------------------"
	set -x; # enable command echo

	NAME=$(basename $X)
	SPEC=$(spec_name ${NAME})
	cp $SPEC $RPMBUILD/SPECS
	rpmbuild --define "_topdir $RPMBUILD" \
		--define "_with_ovis_lib $TMP_ROOT_PREFIX" \
		--define "_with_sos $TMP_ROOT_PREFIX" \
		--define "_with_slurm /opt/slurm" \
		--define "_with_aries_libgpcd $ARIES_LIBGPCD" \
		--define "_with_rca /opt/cray/rca/default" \
		--define "_with_krca /opt/cray/krca/default" \
		--define "_with_cray_hss_devel /opt/cray-hss-devel/default" \
		--define "_with_libpapi $LIBPAPI" \
		--define "_commit_id $COMMIT_ID" \
		-ba $RPMBUILD/SPECS/$SPEC

	case $X in
	sos)
		RPM_PTN="sosdb"
	;;
	*)
		RPM_PTN=""
	;;
	esac
	if test -n "$RPM_PTN"; then
		# install ovis-lib and sosdb as build prerequisite of ldms
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
