%ifarch %ix86
arch=i386
%endif
%ifarch x86_64
arch=x86_64
%endif
flavor=%1
pushd /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/rm
make module \
     SYSSRC=/usr/src/linux SYSOUT=/usr/src/linux-obj/$arch/$flavor \
     KBUILD_EXTMOD=/usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/rm
popd
cp -f /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/rm/Module.symvers /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/Module.symvers
pushd /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor
make $PWD/conftest/headers.h $PWD/conftest/functions.h $PWD/conftest/generic.h \
     $PWD/conftest/macros.h $PWD/conftest/symbols.h $PWD/conftest/types.h $PWD/conftest/patches.h \
     CURDIR=$PWD RM_OUT_DIR=/usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/rm \
     SYSSRC=/usr/src/linux \
     SYSOUT=/usr/src/linux-obj/$arch/$flavor
popd
make -C /usr/src/linux-obj/$arch/$flavor \
     modules \
     M=/usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor \
     SYSSRC=/usr/src/linux \
     SYSOUT=/usr/src/linux-obj/$arch/$flavor \
     RM_OUT_DIR=/usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/rm
install -m 755 -d /lib/modules/%2-$flavor/updates
install -m 644 /usr/src/kernel-modules/nvidia-uvm-%{-v*}-$flavor/nvidia-uvm.ko \
	/lib/modules/%2-$flavor/updates
depmod %2-$flavor
