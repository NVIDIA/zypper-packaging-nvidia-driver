flavor=%1
pushd /usr/src/kernel-modules/nvidia-%{-v*}-$flavor || true
cp -a Makefile{,.tmp} || true
make clean || true
mv Makefile{.tmp,} || true
popd || true
%if 0%{?sle_version} >= 150200
# remove MOK key
if [ -x /usr/bin/mokutil ]; then
  pubkeydir=/var/lib/nvidia-pubkeys
  pubkey=$pubkeydir/MOK-%{name}-%{-v*}-$flavor.der
  mokutil --delete $pubkey --root-pw
fi
%endif
