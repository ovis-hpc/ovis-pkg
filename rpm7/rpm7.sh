#!/bin/bash
#
# This works similar to ./all-autogen*.sh script, but it will generate RPMs
# instead of installing the applications. The resulting RPMs can be found in
# <project-dir>/$BUILD_DIR/rpm7/RPMS
#
# The RPM installation destination is the $PREFIX

BUILD_DIR="build-rpm7"
OVIS_SRC=$(dirname $PWD)/ovis
PREFIX=/opt/ovis

WITH_OVIS_LIB="--with-ovis-lib=$OVIS_SRC/lib/$BUILD_DIR/rpm7/BUILDROOT$PREFIX"
WITH_SOS="--with-sos=$OVIS_SRC/sos/$BUILD_DIR/rpm7/BUILDROOT$PREFIX"

WITH="$WITH_OVIS_LIB $WITH_SOS"

CFLAGS='-g -O3'

# Exit immediately if a command failed
set -e

RPMS_DEST=$PWD/RPM7
rm -rf $RPMS_DEST
mkdir -p $RPMS_DEST

SPEC_SRC_DIR=$PWD
LIST="lib sos ldms baler"
for X in $LIST; do
	echo "----------------------------------"
	echo "$X"
	echo "----------------------------------"
	set -x; # enable command echo
	pushd ../ovis/$X
	./autogen.sh
	mkdir -p $BUILD_DIR
	pushd $BUILD_DIR # We still rely on git-enabled source dir to resolve
			 # git-SHA for individual package build. Until
			 # individual ovis subproject build support SHA.txt and
			 # TAG.txt, we just have to do this.
	rm -rf * # Making sure that the build is clean
	../configure $WITH # doesn't need other options here as this is for
			   # `make dist` only. For the enable/disable
			   # options for each package, please see configure
			   # options in their spec files.
	make dist

	mkdir -p rpm7/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
	ln -f -s ../../automake rpm7/BUILD/automake
	cp *.tar.gz rpm7/SOURCES
	SPEC=${X}.rhel7.spec
	cp $SPEC_SRC_DIR/$SPEC rpm7/SPECS
	QA_RPATHS=0x0003 ; \
	export QA_RPATHS ; \
	rpmbuild --define "_topdir `pwd`/rpm7" \
		--define "_ovis_src $OVIS_SRC" \
		--define "_build_dir $BUILD_DIR" \
		--define "_prefix $PREFIX" \
		--buildroot `pwd`/rpm7/BUILDROOT \
		-ba rpm7/SPECS/$SPEC

	mkdir -p rpm7/BUILDROOT
	pushd rpm7/BUILDROOT
	for Y in ../RPMS/*/*.rpm; do
		# Extract RPM contents so that the dependent programs can link
		# and build.
		echo "-- Extracting $Y --"
		rpm2cpio $Y | cpio -idmv
		mv $Y $RPMS_DEST
	done
	popd # rpm7/BUILDROOT
	popd # $BUILD_DIR
	popd # ../ovis/$X
	set +x; # disable command echo so that it won't print the "for ..." command
	echo "----- DONE -----"
done

echo "Please see the RPMs in $RPMS_DEST"
