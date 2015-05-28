#
# spec file for package nvidia-gfxG04
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# kABI symbols are no longer generated with openSUSE >= 13.1, since they
# became useless with zypper's 'multiversion' feature enabled for the kernel
# as default (multiple kernels can be installed at the same time; with
# different kABI symbols of course!). So it has been decided to match on the
# uname output of the kernel only. We cannot use that one for NVIDIA, since we
# only build against GA kernel. So let's get rid of this requirement.
#
%global __requires_exclude kernel-uname-r*

Name:           nvidia-gfxG04
Version:        346.72
Release:        0
License:        PERMISSIVE-OSI-COMPLIANT
Summary:        NVIDIA graphics driver kernel module for GeForce 400 series and newer
Group:          System/Kernel
Source0:        http://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
Source1:        http://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source3:        preamble
Source4:        pci_ids-%{version}
Source5:        pci_ids-%{version}.new
Source6:        generate-service-file.sh
Source7:        README
Source8:        kmp-filelist
Source9:        kmp-filelist-old
Source10:       kmp-post.sh
Source11:       kmp-post-old.sh
Source12:       my-find-supplements
Source13:       kmp-preun.sh
Source14:       kmp-preun-old.sh
Source15:       kmp-pre.sh
Source16:       alternate-install-present
NoSource:       0
NoSource:       1
NoSource:       6
NoSource:       7
BuildRequires:  kernel-source
BuildRequires:  kernel-syms
BuildRequires:  module-init-tools
BuildRequires:  update-alternatives
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
ExclusiveArch:  %ix86 x86_64
# patch the kmp template
%if 0%{?suse_version} > 1100
%define kmp_template -t
%define kmp_filelist kmp-filelist
%define kmp_post kmp-post.sh
%define kmp_preun kmp-preun.sh
%define kmp_pre kmp-pre.sh
%else
%define kmp_template -s
%define kmp_filelist kmp-filelist-old
%define kmp_post kmp-post-old.sh
%define kmp_preun kmp-preun-old.sh
%define kmp_pre kmp-pre.sh
%endif
%if 0%{!?kmp_template_name:1}
%if 0%{?suse_version} > 1010
%define kmp_template_name /usr/lib/rpm/kernel-module-subpackage
%else
%define kmp_template_name /usr/lib/rpm/rpm-suse-kernel-module-subpackage
%endif
%endif
%(sed -e '/^%%post\>/ r %_sourcedir/%kmp_post' -e '/^%%preun\>/ r %_sourcedir/%kmp_preun' -e '/^%%pre\>/ r %_sourcedir/%kmp_pre' -e '/^Provides: multiversion(kernel)/d' %kmp_template_name >%_builddir/nvidia-kmp-template)
%define x_flavors kdump um debug xen xenpae
%if 0%{!?nvbuild:1}
%define kver %(rpm -q --qf '%%{VERSION}' kernel-source|perl -ne '/(\\d+)\\.(\\d+)\\.(\\d+)?/&&printf "%%d%%02d%%02d\\n",$1,$2,$3')
%if %kver >= 20627
%if %kver < 20631
%define x_flavors kdump um debug
%endif
%endif
%endif
%kernel_module_package %kmp_template %_builddir/nvidia-kmp-template -p %_sourcedir/preamble -f %_sourcedir/%kmp_filelist -x %x_flavors

# supplements no longer depend on the driver
%if 0%{?suse_version} > 1320
%define pci_id_file %_sourcedir/pci_ids-%version
%else
%define pci_id_file %_sourcedir/pci_ids-%version.new
%endif
# rpm 4.9+ using the internal dependency generators
%define __ksyms_supplements %_sourcedir/my-find-supplements %pci_id_file %name
# older rpm
%define __find_supplements %_sourcedir/my-find-supplements %pci_id_file %name

%description
NVIDIA graphics driver kernel module for GeForce 400 and newer

%package KMP
License:        PERMISSIVE-OSI-COMPLIANT
Summary:        NVIDIA graphics driver kernel module for GeForce 400 series and newer
Group:          System/Kernel

%description KMP
NVIDIA graphics driver kernel module for GeForce 400 series and newer

%prep
echo "kver = %kver"
%setup -T -c %{name}-%{version}
%ifarch %ix86
 sh %{SOURCE0} -x
%endif
%ifarch x86_64
 sh %{SOURCE1} -x
%endif
#rm -rf NVIDIA-Linux-x86*-%{version}-*/usr/src/nv/precompiled
mkdir -p source/%{version}
rm -rf NVIDIA-Linux-x86*-%{version}*/kernel/uvm
cp NVIDIA-Linux-x86*-%{version}*/kernel/* source/%{version} || :
pushd source/%{version}
 # mark support as external
 echo "nvidia.ko external" > Module.supported
# IDs have already been added to G03 when we no longer built/published G04
# for sle11 (bnc#920799). Since we now build/publish it again for sle11
# (bnc#929127), we need to make sure that IDs are not registered for both
# driver series G03 and G04. So remove them from G04.
%if 0%{?suse_version} < 1120
 for id in 0x1340 0x1341 \
           0x1380 0x1381 0x1382 \
           0x1390 0x1391 0x1392 0x1393 \
           0x13BA 0x13BB; do
   sed -i /${id}/d %_sourcedir/pci_ids-%{version}
   sed -i /${id}/d %_sourcedir/pci_ids-%{version}.new
 done
%endif
 chmod 755 %_sourcedir/my-find-supplements*
popd
mkdir obj
sed -i -e 's,-o "$ARCH" = "x86_64",-o "$ARCH" = "x86_64" -o "$ARCH" = "x86",' source/*/conftest.sh

%build
export EXTRA_CFLAGS='-DVERSION=\"%{version}\"'
%if 0%{?suse_version} <= 1020
export SYSSRC=/usr/src/linux
%endif
for flavor in %flavors_to_build; do
    rm -rf obj/$flavor
    cp -r source obj/$flavor
    make -C $PWD/obj/$flavor/%{version} conftest/headers.h conftest/functions.h conftest/generic.h conftest/macros.h conftest/symbols.h conftest/types.h conftest/patches.h SYSSRC=/usr/src/linux SYSOUT=/usr/src/linux-obj/%_target_cpu/$flavor
    make -C /usr/src/linux-obj/%_target_cpu/$flavor modules M=$PWD/obj/$flavor/%{version} SYSSRC=/usr/src/linux SYSOUT=/usr/src/linux-obj/%_target_cpu/$flavor
    pushd $PWD/obj/$flavor/%{version}
    make -f Makefile nv-linux.o SYSSRC=/usr/src/linux SYSOUT=/usr/src/linux-obj/%_target_cpu/$flavor
    popd
done

%install
### do not sign the ghost .ko file, it is generated on target system anyway
export BRP_PESIGN_FILES=""
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=updates
export SYSSRC=/usr/src/linux
for flavor in %flavors_to_build; do
    make -C /usr/src/linux-obj/%_target_cpu/$flavor modules_install M=$PWD/obj/$flavor/%{version}
    #install -m 644 $PWD/obj/$flavor/%{version}/{nv-linux.o,nv-kernel.o} \
    #  %{buildroot}/lib/modules/*-$flavor/updates
    mkdir -p %{buildroot}/usr/src/kernel-modules/nvidia-%{version}-${flavor}
    cp -r source/%{version}/* %{buildroot}/usr/src/kernel-modules/nvidia-%{version}-${flavor}
done
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
mkdir -p %{buildroot}/usr/lib/nvidia/
for flavor in %flavors_to_build; do
  echo "blacklist nouveau" > %{buildroot}%{_sysconfdir}/modprobe.d/nvidia-$flavor.conf
  # make it with flavor name or rpmlint complains about not making it conflict
  cp %{SOURCE16} %{buildroot}/usr/lib/nvidia/alternate-install-present-${flavor}
  touch %{buildroot}/usr/lib/nvidia/alternate-install-present
done
%changelog
