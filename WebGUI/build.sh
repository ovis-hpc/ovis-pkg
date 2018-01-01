#!/bin/bash
#
# README
#

# Exit immediately if a command failed
set -e

ARCH=$(uname -m)

RPMBUILD=$PWD/rpmbuild
rm -rf ${RPMBUILD}
mkdir -p $RPMBUILD/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

PREFIX=/var/www/ovis_web_svcs
TMP_ROOT=$PWD/tmproot
rm -rf ${TMP_ROOT}
TMP_ROOT_PREFIX=$TMP_ROOT/${PREFIX}
mkdir -p $TMP_ROOT_PREFIX

function spec_name() {
	echo -n $1.spec
}

LIST="sosdb-ui sosdb-grafana ovis-baler-ui ovis-ldms-ui"
for X in $LIST; do
	echo "----------------------------------"
	echo "$X"
	echo "----------------------------------"
	set -x; # enable command echo

	# First, generate the source tarball
	pushd ../$X
	./autogen.sh
	BUILD_DIR=$PWD/build-rpm
	mkdir -p $BUILD_DIR
	pushd $BUILD_DIR
	rm -rf * # Making sure that the build is clean
	../configure --prefix=${PREFIX}
	make dist

	cp *.tar.gz $RPMBUILD/SOURCES
	popd # $BUILD_DIR
	popd # ../$X

	NAME=$(basename $X)
	SPEC=$(spec_name ${NAME})
	cp $SPEC $RPMBUILD/SPECS
	rpmbuild --define "_topdir $RPMBUILD" \
		-ba $RPMBUILD/SPECS/$SPEC

	set +x; # disable command echo so that it won't print the "for ..." command
	echo "----- DONE -----"
done

echo "FINISH: Please find RPMS and SRPMS in ./rpmbuild/RPMS and ./rpmbuild/SRPMS respectively"
