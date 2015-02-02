flavor=%1
cp -a /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/Makefile{,.tmp} || true
make -C /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor RM_OUT_DIR=/usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/rm clean || true
mv /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/Makefile{.tmp,} || true
