flavor=%1
cp -a /usr/src/kernel-modules/nvidia-%{-v*}-$flavor/Makefile{,.tmp} || true
make -C /usr/src/kernel-modules/nvidia-%{-v*}-$flavor clean || true
mv /usr/src/kernel-modules/nvidia-%{-v*}-$flavor/Makefile{.tmp,} || true

if [ "$1" = 0 ] ; then
    %{_sbindir}/update-alternatives --remove alternate-install-present /usr/lib/nvidia/alternate-install-present-$flavor
fi
