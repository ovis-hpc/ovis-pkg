OVIS Packaging Repository
=========================

This repository currently host only scripts to generate RPM on RHEL7. Please
follow the instructions below to generate RPM for RHEL7.


RPM for RHEL7 instructions
--------------------------

- If submodules are not initialized, please do:
```sh
# assuming that PWD is ovis-pkg
git submodule init ovis
pushd ovis
git submodule init sos
popd
```

- Make sure that submodules are up-to-date:
```sh
# assuming that PWD is ovis-pkg
git submodule update ovis
pushd ovis
git submodule update sos
popd
```

- Call the rpm7.sh script
```sh
# assuming that PWD is ovis-pkg
cd rpm7
./rpm7.sh
ls rpmbuild/RPMS/ # the RPMs are in here.
ls rpmbuild/SRPMS/ # the SRPMs are in here.
```
