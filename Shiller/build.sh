#!/bin/bash
#
# README
#
OVIS_SRC=$(dirname $PWD)/ovis

CFLAGS='-g -O3'
LDFLAGS='-L/usr/local/lib -lm -lpthread'

# Exit immediately if a command failed
set -e

ARCH=$(uname -m)

RPMBUILD=$PWD/rpmbuild
rm -rf ${RPMBUILD}
mkdir -p $RPMBUILD/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

TMP_ROOT=$PWD/tmproot
rm -rf ${TMP_ROOT}
TMP_ROOT_PREFIX=$TMP_ROOT/opt/ovis
mkdir -p $TMP_ROOT_PREFIX

WITH_OVIS_LIB="--with-ovis-lib=$TMP_ROOT_PREFIX"
WITH_SOS="--with-sos=$TMP_ROOT_PREFIX"
WITH_SLURM="--with-slurm=/opt/slurm --enable-jobinfo-slurm"
WITH="$WITH_OVIS_LIB $WITH_SOS $WITH_SLURM --enable-doc --enable-swig"

function pkg_name() {
	case $1 in
	baler)
		echo -n "baler"
	;;
	lib)
		echo -n "ovis-lib"
	;;
	ldms)
		echo -n "ovis-ldms"
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

LIST="sos ovis/lib ovis/ldms"
for X in $LIST; do
	echo "----------------------------------"
	echo "$X"
	echo "----------------------------------"
	set -x; # enable command echo

	# First, generate the source tarball
	pushd ../$X
	./autogen.sh
	BUILD_DIR=$PWD/build-rpm7
	mkdir -p $BUILD_DIR
	pushd $BUILD_DIR
	rm -rf * # Making sure that the build is clean
	../configure LDFLAGS="-L/usr/local/lib -lm -lpthread" $WITH # doesn't need other options here as this is for
			   # `make dist` only. For the enable/disable
			   # options for each package, please see configure
			   # options in their spec files.
	make dist

	cp *.tar.gz $RPMBUILD/SOURCES
	popd # $BUILD_DIR
	popd # ../ovis/$X

	NAME=$(basename $X)
	SPEC=$(spec_name ${NAME})
	cp $SPEC $RPMBUILD/SPECS
	rpmbuild --define "_topdir $RPMBUILD" \
		--define "_with_ovis_lib $TMP_ROOT_PREFIX" \
		--define "_with_sos $TMP_ROOT_PREFIX" \
		-ba $RPMBUILD/SPECS/$SPEC

	case $X in
	ovis/lib)
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
