flavor=%1
pushd /usr/src/kernel-modules/nvidia-%{-v*}-$flavor || true
cp -a Makefile{,.tmp} || true
make clean || true
mv Makefile{.tmp,} || true
popd || true
