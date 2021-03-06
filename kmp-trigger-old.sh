# get rid of broken weak-updates symlinks created in some %post apparently;
# either by kmp itself or by kernel package update
for i in $(find /lib/modules/*/weak-updates -type l 2> /dev/null); do
  test -e $(readlink -f $i) || rm $i
done
%ifarch %ix86
arch=i386
%endif
%ifarch x86_64
arch=x86_64
%endif
flavor=%1
kver=$(make -sC /usr/src/linux-obj/$arch/$flavor kernelrelease)
make -C /usr/src/linux-obj/$arch/$flavor \
     modules \
     M=/usr/src/kernel-modules/nvidia-%{-v*}-$flavor \
     SYSSRC=/lib/modules/$kver/source \
     SYSOUT=/usr/src/linux-obj/$arch/$flavor
pushd /usr/src/kernel-modules/nvidia-%{-v*}-$flavor 
make -f Makefile \
     nv-linux.o \
     SYSSRC=/lib/modules/$kver/source \
     SYSOUT=/usr/src/linux-obj/$arch/$flavor
popd
install -m 755 -d /lib/modules/$kver/updates
install -m 644 /usr/src/kernel-modules/nvidia-%{-v*}-$flavor/nvidia.ko \
	/lib/modules/$kver/updates
depmod $kver

%{_sbindir}/update-alternatives --install /usr/lib/nvidia/alternate-install-present alternate-install-present /usr/lib/nvidia/alternate-install-present-$flavor 11

echo
echo "Modprobe blacklist files have been created at /etc/modprobe.d to \
prevent Nouveau from loading. This can be reverted by deleting \
/etc/modprobe.d/nvidia-*.conf."
echo
echo "*** Reboot your computer and verify that the NVIDIA graphics driver \
can be loaded. ***"
echo

# Let all initrds get generated by regenerate-initrd-posttrans
mkdir -p /run/regenerate-initrd
touch /run/regenerate-initrd/all

