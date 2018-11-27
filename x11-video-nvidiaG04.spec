#
# spec file for package x11-video-nvidiaG04
#
# Copyright (c) 2017 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%if 0%{?suse_version} > 1010 || "%_repository" == "SLE_10_XORG7"
%define xlibdir %{_libdir}/xorg
%else
%define xlibdir %{_prefix}/X11R6/%{_lib}
%endif

%if 0%{?suse_version} < 1130
%define GENERATE_IDENTITY_MAP 1
%else
%define GENERATE_IDENTITY_MAP 0
%endif

%if 0%{?suse_version} >= 1315
%define xmodulesdir %{xlibdir}/modules
%else
%define xmodulesdir %{xlibdir}/modules/updates
%endif

Name:           x11-video-nvidiaG04
Version:        390.87
Release:        0
License:        SUSE-NonFree
Summary:        NVIDIA graphics driver for GeForce 400 series and newer
URL:            https://www.nvidia.com/object/unix.html
Group:          System/Libraries
Source0:        http://download.nvidia.com/XFree86/Linux-x86/%{version}/NVIDIA-Linux-x86-%{version}.run
Source1:        http://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source2:        pci_ids-%{version}.new
Source3:        nvidia-settings.desktop
Source4:        generate-service-file.sh
Source5:        README
Source6:        Xwrapper
Source7:        pci_ids-%{version}
Source8:        rpmlintrc
Source9:        libvdpau-0.4.tar.gz
Source10:       vdpauinfo-0.0.6.tar.gz
Source11:       pci_ids-%{version}.legacy
NoSource:       0
NoSource:       1
NoSource:       4
NoSource:       5
Patch:          vdpauinfo-missing-lX11.diff
Patch1:         U_Use-secure_getenv-3-to-improve-security.patch
BuildRequires:  update-desktop-files
%if 0%{?suse_version} < 1130
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  graphviz
BuildRequires:  pkgconfig
BuildRequires:  texlive
BuildRequires:  xorg-x11-devel
%endif
%if 0%{?suse_version} < 1020
BuildRequires:  xorg-x11-compat70-devel
%endif
Requires:       3ddiag
Requires:       nvidia-computeG04 = %{version}
Requires:       nvidia-gfxG04-kmp = %{version}
Provides:       nvidia_driver = %{version}
Provides:       nvidia-xconfig = %{version}
Provides:       nvidia-settings = %{version}
Obsoletes:      nvidia-modprobe <= 319.37
Provides:       nvidia-modprobe = %{version}
Conflicts:      x11-video-nvidia
Conflicts:      x11-video-nvidiaG01
Conflicts:      x11-video-nvidiaG02
Conflicts:      x11-video-nvidiaG03
Conflicts:      fglrx_driver
Requires:       libvdpau1
ExclusiveArch:  %ix86 x86_64
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package provides the closed-source NVIDIA graphics driver
for GeForce 400 series and newer GPUs.

%package -n nvidia-computeG04
Summary:        NVIDIA driver for computing with GPGPU
Group:          System/Libraries
%if 0%{?suse_version} > 1220
Requires:       nvidia-gfxG04-kmp = %{version}
%else
Requires:       nvidia-gfxG04-kmp
%endif
# to provide a hint about split to zypper dup:
Provides:       x11-video-nvidiaG04:/usr/lib/libcuda.so
Conflicts:      nvidia-computeG02
Conflicts:      nvidia-computeG03
Conflicts:      libOpenCL1

%description -n nvidia-computeG04
NVIDIA driver for computing with GPGPUs using CUDA or OpenCL.

%package -n nvidia-glG04
Summary:        NVIDIA OpenGL libraries for OpenGL acceleration
Group:          System/Libraries
%if 0%{?suse_version} > 1220
Requires:       nvidia-gfxG04-kmp = %{version}
%else
Requires:       nvidia-gfxG04-kmp
%endif
%if 0%{?suse_version} >= 1315
Requires(post):   update-alternatives
Requires(postun): update-alternatives
# on Optimus we want to switch back to X.Org's libglx.so (bsc#1111471)
Requires(post):   xorg-x11-server
%endif
# to provide a hint about split to zypper dup:
Provides:       x11-video-nvidiaG04:/{_prefix}/X11R6/%{_lib}/libGL.so.1
Conflicts:      nvidia-glG03
# needed for Optimus systems once NVIDIA's libs get disabled (our default);
# these packages won't get installed when adding NVIDIA's repository before
# the installation, which e.g. happens on SLED (bsc#1111471)
Recommends:     Mesa-libGL1
Recommends:     Mesa-libEGL1
Recommends:     Mesa-libGLESv1_CM1
Recommends:     Mesa-libGLESv2-2
AutoReq: no

%description -n nvidia-glG04
This package provides the NVIDIA OpenGL libraries to allow OpenGL
acceleration under the closed-source NVIDIA drivers.

%package -n nvidia-diagnosticG04
Summary:        Diagnostic utilities for the NVIDIA driver
Group:          System/Libraries
%if 0%{?suse_version} > 1220
Requires:       nvidia-gfxG04-kmp = %{version}
%else
Requires:       nvidia-gfxG04-kmp
%endif
Obsoletes:      nvidia-diagnosticG03
Conflicts:      nvidia-diagnosticG03

%description -n nvidia-diagnosticG04
Diagnostic utilities for the NVIDIA driver.

%package -n libvdpau1
License:        X11/MIT
Summary:        VDPAU wrapper and trace libraries
Group:          System/Libraries

%description -n libvdpau1
This package contains the libvdpau wrapper library and the
libvdpau_trace debugging library, along with the header files needed to
build VDPAU applications.  To actually use a VDPAU device, you need a
vendor-specific implementation library.  Currently, this is always
libvdpau_nvidia.  You can override the driver name by setting the
VDPAU_DRIVER environment variable.

%package -n libvdpau-devel
License:        X11/MIT
Summary:        VDPAU wrapper development files
Group:          Development/Libraries/X11
Requires:       libvdpau1

%description -n libvdpau-devel
Note that this package only contains the VDPAU headers that are
required to build applications. At runtime, the shared libraries are
needed too and may be installed using the proprietary nVidia driver
packages.

%package -n libvdpau_trace1
License:        X11/MIT
Summary:        VDPAU trace library
Group:          System/Libraries
Requires:       libvdpau1

%description -n libvdpau_trace1
This package provides the library for tracing VDPAU function calls.

%prep
%setup -T -c %{name}-%{version}
%ifarch %ix86
 sh %{SOURCE0} -x
%endif
%ifarch x86_64
 sh %{SOURCE1} -x
%endif
%if 0%{?suse_version} < 1130
tar xvf %{SOURCE9}
tar xvf %{SOURCE10}
pushd vdpauinfo-*
%patch -p0
popd
pushd libvdpau-*
%patch1 -p1
popd
%endif

%build
# nothing

%install
# no longer alter, i.e. strip NVIDIA's libraries
export NO_BRP_STRIP_DEBUG=true
%if 0%{?suse_version} < 1130
pushd libvdpau-*
  %configure
  make %{?jobs:-j%jobs}
  %makeinstall
  rm %{buildroot}%{_libdir}/libvdpau.la
  rm %{buildroot}%{_libdir}/vdpau/libvdpau_trace.la
popd
%endif
cd NVIDIA-Linux-x86*-%{version}
# would be nice if it worked ...
#./nvidia-installer \
#	--accept-license \
#	--expert \
#	--no-questions \
#	--ui=none \
#	--no-precompiled-interface \
#	--no-runlevel-check \
#	--no-rpms \
#	--no-backup \
#	--no-network \
#	--no-recursion \
#	--no-kernel-module \
#	--log-file-name=$PWD/log \
#	--x-prefix=%{buildroot}%{_prefix}/X11R6 \
#	--opengl-prefix=%{buildroot}%{_prefix} \
#	--utility-prefix=%{buildroot}%{_prefix}
# only to be used by GLVND
rm -f libGL.so.1.* 32/libGL.so.1.*
rm -f libGLX.so.0 32/libGLX.so.0
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_prefix}/X11R6/lib
install -d %{buildroot}%{_prefix}/lib/tls
install -d %{buildroot}%{_prefix}/X11R6/%{_lib}
install -d %{buildroot}%{_libdir}/tls
install -d %{buildroot}%{_prefix}/lib/vdpau
install -d %{buildroot}%{_libdir}/vdpau
install -d %{buildroot}%{xmodulesdir}/drivers
install -d %{buildroot}%{xmodulesdir}/extensions
install -d %{buildroot}%{_sysconfdir}/OpenCL/vendors/
install -d %{buildroot}%{_datadir}/nvidia
install -d %{buildroot}%{_datadir}/glvnd/egl_vendor.d
install nvidia-settings %{buildroot}%{_bindir}
install nvidia-bug-report.sh %{buildroot}%{_bindir}
install nvidia-xconfig %{buildroot}%{_bindir}
install nvidia-smi %{buildroot}%{_bindir}
install nvidia-debugdump %{buildroot}%{_bindir}
install nvidia-cuda-mps-control %{buildroot}%{_bindir}
install nvidia-cuda-mps-server %{buildroot}%{_bindir}
install nvidia-persistenced %{buildroot}%{_bindir}
install libnvidia-tls.so.* %{buildroot}%{_libdir}/tls
install libnvidia* %{buildroot}%{_libdir}
install libcuda* %{buildroot}%{_libdir}
install libOpenCL* %{buildroot}%{_libdir}
install libnvcuvid* %{buildroot}%{_libdir}
install libnvidia-ml* %{buildroot}%{_libdir}
install libvdpau_nvidia.so* %{buildroot}%{_libdir}/vdpau
install libnvoptix.so.%{version} %{buildroot}%{_libdir}
# nvidia-modprobe must be setuid root to function correctly
install -m 4755 nvidia-modprobe %{buildroot}%{_bindir}
# Bug #596481
ln -s vdpau/libvdpau_nvidia.so.1 %{buildroot}%{_libdir}/libvdpau_nvidia.so
# the GL lib from Mesa is in /usr/%{_lib} so we install in /usr/X11R6/%{_lib}
rm libGL.la
install libGL* %{buildroot}%{_prefix}/X11R6/%{_lib}
# still a lot of applications make a dlopen to the .so file
ln -snf libGL.so.1 %{buildroot}%{_prefix}/X11R6/%{_lib}/libGL.so
ln -snf libGL.so.%{version} %{buildroot}%{_prefix}/X11R6/%{_lib}/libGL.so.1
ln -snf libGLX_nvidia.so.%{version} %{buildroot}%{_prefix}/X11R6/%{_lib}/libGLX_nvidia.so.0
ln -snf libGLX_nvidia.so.%{version} %{buildroot}%{_prefix}/X11R6/%{_lib}/libGLX_indirect.so.0
ln -snf libOpenGL.so.0 %{buildroot}%{_prefix}/X11R6/%{_lib}/libOpenGL.so
ln -snf libnvidia-ptxjitcompiler.so.1 %{buildroot}%{_libdir}/libnvidia-ptxjitcompiler.so
# same for libOpenGL/libcuda/libnvcuvid
ln -snf libOpenCL.so.1 %{buildroot}%{_libdir}/libOpenCL.so
ln -snf libcuda.so.1   %{buildroot}%{_libdir}/libcuda.so
ln -snf libnvcuvid.so.1 %{buildroot}%{_libdir}/libnvcuvid.so
# NVML library for Tesla compute products (new since 270.xx)
ln -s libnvidia-ml.so.1  %{buildroot}%{_libdir}/libnvidia-ml.so
# Optical flow library
ln -s libnvidia-of.so.1  %{buildroot}%{_libdir}/libnvidia-of.so
# EGL/GLES 64bit new since 340.xx
install libEGL.so.%{version} %{buildroot}%{_prefix}/X11R6/%{_lib}
install libEGL_nvidia.so.* %{buildroot}%{_prefix}/X11R6/%{_lib}
install 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d
install libGLESv1_CM* %{buildroot}%{_prefix}/X11R6/%{_lib}
install libGLESv2* %{buildroot}%{_prefix}/X11R6/%{_lib}
install libOpenGL* %{buildroot}%{_prefix}/X11R6/%{_lib}
%if 0%{?suse_version} < 1100
install libnvidia-wfb.so.%{version} \
  %{buildroot}%{xmodulesdir}
ln -sf libnvidia-wfb.so.%{version} %{buildroot}%{xmodulesdir}/libwfb.so
%endif
install nvidia_drv.so %{buildroot}%{xmodulesdir}/drivers
%if 0%{?suse_version} < 1315
install libglxserver_nvidia.so.%{version} \
  %{buildroot}%{xmodulesdir}/extensions/
ln -sf libglxserver_nvidia.so.%{version} %{buildroot}%{xmodulesdir}/extensions/libglxserver_nvidia.so
%else
mkdir -p %{buildroot}%{xmodulesdir}/extensions/nvidia
install libglxserver_nvidia.so.%{version} \
  %{buildroot}%{xmodulesdir}/extensions/nvidia/nvidia-libglx.so
%endif
%ifarch x86_64
install 32/libnvidia-tls.so.* %{buildroot}%{_prefix}/lib/tls
install 32/libnvidia* %{buildroot}%{_prefix}/lib
install 32/libcuda* %{buildroot}%{_prefix}/lib
install 32/libOpenCL* %{buildroot}%{_prefix}/lib
install 32/libnvcuvid* %{buildroot}%{_prefix}/lib
install 32/libvdpau_nvidia.so* %{buildroot}%{_prefix}/lib/vdpau
install 32/libGL* %{buildroot}%{_prefix}/X11R6/lib
install 32/libEGL.so.%{version} %{buildroot}%{_prefix}/X11R6/lib
install 32/libEGL_nvidia.so.* %{buildroot}%{_prefix}/X11R6/lib
install 32/libGLESv1_CM* %{buildroot}%{_prefix}/X11R6/lib
install 32/libGLESv2* %{buildroot}%{_prefix}/X11R6/lib
install 32/libOpenGL* %{buildroot}%{_prefix}/X11R6/lib
# Bug #596481
ln -s vdpau/libvdpau_nvidia.so.1 %{buildroot}%{_prefix}/lib/libvdpau_nvidia.so
# still a lot of applications make a dlopen to the .so file
ln -snf libGL.so.1 %{buildroot}%{_prefix}/X11R6/lib/libGL.so
ln -snf libGL.so.%{version} %{buildroot}%{_prefix}/X11R6/lib/libGL.so.1
ln -snf libGLX_nvidia.so.%{version} %{buildroot}%{_prefix}/X11R6/lib/libGLX_nvidia.so.0
ln -snf libGLX_nvidia.so.%{version} %{buildroot}%{_prefix}/X11R6/lib/libGLX_indirect.so.0
ln -snf libOpenGL.so.0 %{buildroot}%{_prefix}/X11R6/lib/libOpenGL.so
ln -snf libnvidia-ptxjitcompiler.so.1 %{buildroot}%{_prefix}/lib/libnvidia-ptxjitcompiler.so
# same for libOpenCL/libcuda/libnvcuvid
ln -snf libOpenCL.so.1 %{buildroot}%{_prefix}/lib/libOpenCL.so
ln -snf libcuda.so.1   %{buildroot}%{_prefix}/lib/libcuda.so
ln -snf libnvcuvid.so.1 %{buildroot}%{_prefix}/lib/libnvcuvid.so
%endif
install -d %{buildroot}%{_datadir}/doc/packages/%{name}
cp -a html %{buildroot}%{_datadir}/doc/packages/%{name}
install -m 644 LICENSE %{buildroot}%{_datadir}/doc/packages/%{name}
install -m 644 nvidia-persistenced-init.tar.bz2 \
  %{buildroot}%{_datadir}/doc/packages/%{name}
install -d %{buildroot}/%{_mandir}/man1
install -m 644 *.1.gz %{buildroot}/%{_mandir}/man1
%suse_update_desktop_file -i nvidia-settings System SystemSetup
install -d %{buildroot}%{_datadir}/pixmaps
install -m 644 nvidia-settings.png \
  %{buildroot}%{_datadir}/pixmaps
install -m 644 nvidia-application-profiles-%{version}-{rc,key-documentation} \
  %{buildroot}%{_datadir}/nvidia
/sbin/ldconfig -n %{buildroot}%{_libdir}
/sbin/ldconfig -n %{buildroot}%{_libdir}/vdpau
/sbin/ldconfig -n %{buildroot}%{_prefix}/X11R6/%{_lib}
%ifarch x86_64
/sbin/ldconfig -n %{buildroot}%{_prefix}/lib
/sbin/ldconfig -n %{buildroot}%{_prefix}/lib/vdpau
/sbin/ldconfig -n %{buildroot}%{_prefix}/X11R6/lib
%endif
%if %GENERATE_IDENTITY_MAP
mkdir -p %{buildroot}%{_datadir}/sax/sysp/maps/update/ \
         %{buildroot}%{_datadir}/sax/api/data/cdb/ \
         %{buildroot}%{_localstatedir}/lib/hardware/ids
> %{buildroot}%{_datadir}/sax/sysp/maps/update/Identity.map.10.%{name}
> %{buildroot}%{_datadir}/sax/api/data/cdb/Cards.10.%{name}
> %{buildroot}%{_localstatedir}/lib/hardware/ids/10.%{name}
%if 0%{?suse_version} > 1320 || (0%{?suse_version} == 1315 && 0%{?is_opensuse})
%if 0%{?suse_version} > 1500
(cat %_sourcedir/pci_ids-%{version}.legacy; \
%else
(cat %_sourcedir/pci_ids-%{version}; \
%endif
%else
(cat %_sourcedir/pci_ids-%{version}.new; \
%endif
) | \
while read line; do
  VID=0x10de
  NAME=NVIDIA
  SERVER=nvidia
  DEVICE=$(echo $line|awk '{for (i=2;i<NF;i++) printf("%s ",$i); printf("%s",$NF)}')
  DID=$(echo $line|awk '{print $1}'|tr [[:upper:]] [[:lower:]] | sort -u)
  cat >> %{buildroot}%{_datadir}/sax/sysp/maps/update/Identity.map.10.%{name} << EOF
NAME=${NAME}&DEVICE=${DEVICE}&VID=${VID}&DID=${DID}&SERVER=${SERVER}&EXT=&OPT=&RAW=&PROFILE=&SCRIPT3D=&PACKAGE3D=&FLAG=DEFAULT
NAME=${NAME}&DEVICE=${DEVICE}&VID=${VID}&DID=${DID}&SERVER=${SERVER}&EXT=&OPT=&RAW=&PROFILE=&SCRIPT3D=&PACKAGE3D=&FLAG=3D
EOF
  cat >> %{buildroot}%{_datadir}/sax/api/data/cdb/Cards.10.%{name} << EOF
${NAME}:${DEVICE} {
 Driver    = ${SERVER}
 Flag      = 3D
 3DDriver  = ${SERVER}
}
EOF
  cat >> %{buildroot}%{_localstatedir}/lib/hardware/ids/10.%{name} << EOF
 vendor.id              pci ${VID}
&device.id              pci ${DID}
+device.name            ${DEVICE}
+driver.xfree           4|${SERVER}
+driver.xfree           4|${SERVER}|3d
EOF
echo >> %{buildroot}%{_localstatedir}/lib/hardware/ids/10.%{name}
done
%endif
%if 0%{?suse_version} > 1010
%if 0%{?suse_version} < 1330
install -m 755 $RPM_SOURCE_DIR/Xwrapper %{buildroot}%{_bindir}/X.%{name}
%endif
%else
mkdir -p %{buildroot}%{_prefix}/X11R6/bin
install -m 755 $RPM_SOURCE_DIR/Xwrapper %{buildroot}%{_prefix}/X11R6/bin/X.%{name}
%endif
install -m 644 nvidia.icd \
  %{buildroot}%{_sysconfdir}/OpenCL/vendors/
%if 0%{?suse_version} > 1140
# Create /etc/ld.so.conf.d/nvidia-gfxG04
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat > %{buildroot}%{_sysconfdir}/ld.so.conf.d/nvidia-gfxG04.conf <<EOF
%{_prefix}/X11R6/%{_lib}
%ifarch s390x sparc64 x86_64 ppc64
%{_prefix}/X11R6/lib
%endif
%ifarch ppc
%{_prefix}/X11R6/lib64
%endif
EOF
%endif
%if 0%{?suse_version} < 1130
pushd ../vdpauinfo-*
%configure \
VDPAU_CFLAGS=-I$RPM_BUILD_ROOT/usr/include \
VDPAU_LIBS="-L%{_prefix}/X11R6/%{_lib} -L$RPM_BUILD_ROOT/%{_libdir} -lvdpau -lX11"
make %{?jobs:-j%jobs}
%makeinstall
popd
%endif
%if 0%{?diagnostic}
install    -m 0755 -d                               $RPM_BUILD_ROOT/usr/share/nvidia/diagnostic
install -p -m 0655 diagnostic/libnvvs-diagnostic*   $RPM_BUILD_ROOT/usr/share/nvidia/diagnostic
%endif
# get rid of gtk3 deps on sle11 (bnc#929127)
%if 0%{?suse_version} < 1120
rm %{buildroot}/%{_libdir}/libnvidia-gtk3.so.%{version}
%endif
# Vulkan driver config (boo#1051988)
mkdir -p %{buildroot}/etc/vulkan/icd.d/
%if 0%{?suse_version} >= 1330
sed 's/__NV_VK_ICD__/libGLX_nvidia.so.0/' nvidia_icd.json.template > %{buildroot}/etc/vulkan/icd.d/nvidia_icd.json
%else
sed 's/__NV_VK_ICD__/libGL.so.1/' nvidia_icd.json.template > %{buildroot}/etc/vulkan/icd.d/nvidia_icd.json
%endif
# EGL driver config
mkdir -p %{buildroot}/%{_datadir}/egl/egl_external_platform.d
install -m 644 10_nvidia_wayland.json %{buildroot}/%{_datadir}/egl/egl_external_platform.d
# use libglvnd on TW/sle15
%if 0%{?suse_version} >= 1330
rm %{buildroot}/etc/ld.so.conf.d/nvidia-gfxG04.conf \
   %{buildroot}/usr/X11R6/lib*/libEGL.so.* \
   %{buildroot}/usr/X11R6/lib*/libGL.so* \
   %{buildroot}/usr/X11R6/lib*/libGLESv1_CM.so.* \
   %{buildroot}/usr/X11R6/lib*/libGLESv2.so.* \
   %{buildroot}/usr/X11R6/lib*/libGLdispatch.so.* \
   %{buildroot}/usr/X11R6/lib*/libOpenGL.so.*
   mv %{buildroot}/usr/X11R6/%{_lib}/* %{buildroot}/%{_libdir}/
%ifarch x86_64
   mv %{buildroot}/usr/X11R6/lib/*   %{buildroot}/%{_prefix}/lib/
%endif
   rmdir %{buildroot}/usr/X11R6/lib* \
         %{buildroot}/usr/X11R6
   mkdir -p %{buildroot}/%{_datadir}/glvnd/egl_vendor.d
   install -m 644 10_nvidia.json %{buildroot}/%{_datadir}/glvnd/egl_vendor.d
%endif

%posttrans
/sbin/ldconfig
if [ -f etc/X11/xorg.conf ]; then
  test -f etc/X11/xorg.conf.nvidia-post || \
    cp etc/X11/xorg.conf etc/X11/xorg.conf.nvidia-post
fi
# if configuration for proprietary driver already exists, bring it back
# (Bug #270040, comments #91/92)
if [ -f etc/X11/xorg.conf.nvidia-postun ]; then
  mv etc/X11/xorg.conf.nvidia-postun etc/X11/xorg.conf
  # Remove nvidia-xconfig header from past xorg.conf.postun files
  # so switch2nvidia can find "# SaX" token. Can eventually remove.
  sed -i -e '/^# nvidia-xconfig:/d' etc/X11/xorg.conf
  sed -i -e '1{/^$/d}' etc/X11/xorg.conf
fi
test -x usr/bin/switch2nvidia && usr/bin/switch2nvidia
# Bug #449486
if grep -q fbdev etc/X11/xorg.conf; then
  test -x usr/bin/nvidia-xconfig && usr/bin/nvidia-xconfig -s
  # Remove nvidia-xconfig header so switch2nvidia can find "# SaX" token
  sed -i -e '/^# nvidia-xconfig:/d' etc/X11/xorg.conf
  sed -i -e '1{/^$/d}' etc/X11/xorg.conf
fi
# Bug #345125
test -f %{xlibdir}/modules/drivers/nvidia_drv.so && \
  touch %{xlibdir}/modules/drivers/nvidia_drv.so
test -f %{xmodulesdir}/drivers/nvidia_drv.so && \
  touch %{xmodulesdir}/drivers/nvidia_drv.so
if ls var/lib/hardware/ids/* &> /dev/null; then
  >  var/lib/hardware/hd.ids
  for i in var/lib/hardware/ids/*; do
    cat $i >> var/lib/hardware/hd.ids
  done
fi
%if 0%{?suse_version} < 1330
test -f etc/sysconfig/displaymanager && \
. etc/sysconfig/displaymanager
if [ "${DISPLAYMANAGER_XSERVER}" == "X.%{name}" ]; then
  # broken entry in /etc/sysconfig/displaymanager:DISPLAYMANAGER_XSERVER
  # use a sane default instead
  DISPLAYMANAGER_XSERVER=Xorg
fi
%if 0%{?suse_version} > 1010
sed -i s/REPLACE_ME/${DISPLAYMANAGER_XSERVER}/g usr/bin/X.%{name}
%else
sed -i s/REPLACE_ME/${DISPLAYMANAGER_XSERVER}/g usr/X11R6/bin/X.%{name}
%endif
test -f etc/sysconfig/displaymanager && \
sed -i 's/DISPLAYMANAGER_XSERVER=.*/DISPLAYMANAGER_XSERVER=X.%{name}/g' \
       etc/sysconfig/displaymanager
%if 0%{?suse_version} > 1010
test -x /etc/X11/xdm/SuSEconfig.xdm && \
/etc/X11/xdm/SuSEconfig.xdm
%else
test -x /sbin/conf.d/SuSEconfig.xdm && \
SuSEconfig --module xdm
%endif
%endif
exit 0

%postun
/sbin/ldconfig
if [ "$1" -eq 0 ]; then
  test -x usr/bin/switch2nv && usr/bin/switch2nv
  if ls var/lib/hardware/ids/* &> /dev/null; then
    >  var/lib/hardware/hd.ids
    for i in var/lib/hardware/ids/*; do
      cat $i >> var/lib/hardware/hd.ids
    done
  else
    rm -f var/lib/hardware/hd.ids
  fi
  test -f etc/X11/xorg.conf && \
    cp etc/X11/xorg.conf etc/X11/xorg.conf.nvidia-postun
  if [ -r etc/X11/xorg.conf.nvidia-post ]; then
    mv etc/X11/xorg.conf.nvidia-post etc/X11/xorg.conf
%if 0%{?suse_version} < 1130
  else
    sax2 -a -r
%endif
  fi
  if test -x /opt/gnome/bin/gnome-xgl-switch; then
    /opt/gnome/bin/gnome-xgl-switch --disable-xgl
  elif test -x /usr/bin/xgl-switch; then
    /usr/bin/xgl-switch --disable-xgl
  fi
  # Make sure that after driver uninstall /var/lib/X11/X link points
  # to a valid Xserver binary again (bnc#903732)
%if 0%{?suse_version} > 1010
%if 0%{?suse_version} < 1330
  test -x /etc/X11/xdm/SuSEconfig.xdm && \
  /etc/X11/xdm/SuSEconfig.xdm
%endif
%else
  test -x /sbin/conf.d/SuSEconfig.xdm && \
  SuSEconfig --module xdm
%endif
fi
exit 0

%post -n nvidia-computeG04 -p /sbin/ldconfig

%postun -n nvidia-computeG04 -p /sbin/ldconfig

%posttrans -n nvidia-glG04
%if 0%{?suse_version} >= 1315
%_sbindir/update-alternatives \
    --force --install %{_libdir}/xorg/modules/extensions/libglx.so libglx.so %{_libdir}/xorg/modules/extensions/nvidia/nvidia-libglx.so 100
# make sure nvidia becomes the default (in case the link group is/was still in manual mode)
%_sbindir/update-alternatives \
      --set libglx.so %{_libdir}/xorg/modules/extensions/nvidia/nvidia-libglx.so
# On Optimus systems disable NVIDIA driver/libs completely by default (bnc#902667)
if lspci -n | grep -e '^..:..\.. 0300: ' | cut -d " "  -f3 | cut -d ":" -f1 | grep -q 8086; then
  %_sbindir/update-alternatives \
      --set libglx.so %{_libdir}/xorg/modules/extensions/xorg/xorg-libglx.so
  sed -i 's/\(^\/.*\)/#\1/g' %{_sysconfdir}/ld.so.conf.d/nvidia-gfxG04.conf
fi
%endif
/sbin/ldconfig

%postun -n nvidia-glG04
/sbin/ldconfig
%if 0%{?suse_version} >= 1315
if [ "$1" = 0 ] ; then
    # Avoid accidental removal of G<n+1> alternative (bnc#802624)
    if [ ! -f %{_libdir}/xorg/modules/extensions/nvidia/nvidia-libglx.so ]; then
	"%_sbindir/update-alternatives" --remove libglx.so %{_libdir}/xorg/modules/extensions/nvidia/nvidia-libglx.so
    fi
fi
%endif

%post -n libvdpau1 -p /sbin/ldconfig

%postun  -n libvdpau1 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc %{_datadir}/doc/packages/%{name}
%doc %{_mandir}/man1/*
%exclude %{_mandir}/man1/nvidia-cuda-mps-control.1.gz
%dir %{_datadir}/nvidia
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-rc
%{_datadir}/nvidia/nvidia-application-profiles-%{version}-key-documentation
%if 0%{?suse_version} > 1010
%if 0%{?suse_version} < 1330
%{_bindir}/X.%{name}
%endif
%else
%{_prefix}/X11R6/bin/X.%{name}
%endif
%{_bindir}/nvidia*
%exclude %{_bindir}/nvidia-modprobe
%exclude %{_bindir}/nvidia-smi
%exclude %{_bindir}/nvidia-cuda-mps-control
%exclude %{_bindir}/nvidia-cuda-mps-server
%if 0%{?suse_version} > 1310
%if 0%{?suse_version} < 1330
%dir %{_prefix}/X11R6/
%dir %{_prefix}/X11R6/%{_lib}
%endif
%endif
%if 0%{?suse_version} < 1330
%{_prefix}/X11R6/%{_lib}/lib*
%exclude %{_prefix}/X11R6/%{_lib}/libGL.so*
%exclude %{_prefix}/X11R6/%{_lib}/libGLX_nvidia.so*
%exclude %{_prefix}/X11R6/%{_lib}/libGLdispatch.so*
%exclude %{_prefix}/X11R6/%{_lib}/libEGL.so*
%exclude %{_prefix}/X11R6/%{_lib}/libGLESv1_CM.so*
%exclude %{_prefix}/X11R6/%{_lib}/libGLESv2.so*
%exclude %{_prefix}/X11R6/%{_lib}/libGLESv1_CM_nvidia.so*
%exclude %{_prefix}/X11R6/%{_lib}/libGLESv2_nvidia.so*
%exclude %{_prefix}/X11R6/%{_lib}/libOpenGL.so*
%else
%exclude %{_prefix}/%{_lib}/libGLX_nvidia.so*
%exclude %{_prefix}/%{_lib}/libEGL_nvidia.so*
%exclude %{_prefix}/%{_lib}/libGLESv1_CM_nvidia.so*
%exclude %{_prefix}/%{_lib}/libGLESv2_nvidia.so*
%endif
%exclude %{_libdir}/libnvidia-glcore.so*
%exclude %{_libdir}/libnvidia-ifr.so*
%exclude %{_libdir}/libnvidia-fbc.so*
%exclude %{_libdir}/libnvidia-egl-wayland.so*
%exclude %{_libdir}/libnvidia-gtk*
%exclude %{_libdir}/libnvoptix.so*
%dir %{_libdir}/vdpau
%{_libdir}/lib*
%{_libdir}/vdpau/*
%exclude %{_libdir}/libnvidia-tls.so*
%exclude %{_libdir}/libcuda.so*
%exclude %{_libdir}/libOpenCL.so*
%exclude %{_libdir}/libnvidia-ml.so*
%exclude %{_libdir}/libnvidia-opencl.so*
%exclude %{_libdir}/libnvidia-fatbinaryloader.so*
%exclude %{_libdir}/libnvidia-glsi.so*
%exclude %{_libdir}/libnvidia-eglcore.so*
%exclude %{_libdir}/libnvidia-ptxjitcompiler.so*
%ifarch x86_64
%if 0%{?suse_version} > 1310
%if 0%{?suse_version} < 1330
%dir %{_prefix}/X11R6/lib
%endif
%endif
%if 0%{?suse_version} < 1330
%{_prefix}/X11R6/lib/lib*
%exclude %{_prefix}/X11R6/lib/libGL.so*
%exclude %{_prefix}/X11R6/lib/libGLX_nvidia.so*
%exclude %{_prefix}/X11R6/lib/libGLdispatch.so*
%exclude %{_prefix}/lib/libnvidia-ml.so*
%exclude %{_prefix}/lib/libnvidia-opencl.so*
%exclude %{_prefix}/X11R6/lib/libEGL.so*
%exclude %{_prefix}/X11R6/lib/libGLESv1_CM.so*
%exclude %{_prefix}/X11R6/lib/libGLESv2.so*
%exclude %{_prefix}/X11R6/lib/libGLESv1_CM_nvidia.so*
%exclude %{_prefix}/X11R6/lib/libGLESv2_nvidia.so*
%exclude %{_prefix}/X11R6/lib/libOpenGL.so*
%else
%exclude %{_prefix}/lib/libGLX_nvidia.so*
%exclude %{_prefix}/lib/libEGL_nvidia.so*
%exclude %{_prefix}/lib/libGLESv1_CM_nvidia.so*
%exclude %{_prefix}/lib/libGLESv2_nvidia.so*
%endif
%exclude %{_prefix}/lib/libnvidia-glcore.so*
%exclude %{_prefix}/lib/libnvidia-ifr.so*
%exclude %{_prefix}/lib/libnvidia-eglcore.so*
%exclude %{_prefix}/lib/libnvidia-glsi.so*
%dir %{_prefix}/lib/vdpau
%{_prefix}/lib/lib*
%{_prefix}/lib/vdpau/*
%exclude %{_prefix}/lib/libnvidia-tls.so*
%exclude %{_prefix}/lib/libcuda.so*
%exclude %{_prefix}/lib/libOpenCL.so*
%exclude %{_prefix}/lib/libnvidia-ml.so*
%exclude %{_prefix}/lib/libnvidia-opencl.so*
%exclude %{_prefix}/lib/libnvidia-fatbinaryloader.so*
%exclude %{_prefix}/lib/libnvidia-ptxjitcompiler.so*
%endif
%if 0%{?suse_version} > 1010 || "%_repository" == "SLE_10_XORG7"
%dir %{xlibdir}
%endif
%dir %{xlibdir}/modules
%dir %{xmodulesdir}
%if 0%{?suse_version} < 1100
%{xmodulesdir}/libnvidia-wfb.so.%{version}
%{xmodulesdir}/libwfb.so
%endif
%{xmodulesdir}/drivers
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*.png
%if %GENERATE_IDENTITY_MAP
%dir %{_datadir}/sax
%dir %{_datadir}/sax/api/
%dir %{_datadir}/sax/api/data
%dir %{_datadir}/sax/sysp
%dir %{_datadir}/sax/sysp/maps
%dir %{_localstatedir}/lib/hardware
%{_datadir}/sax/api/data/cdb/
%{_datadir}/sax/sysp/maps/update/
%{_localstatedir}/lib/hardware/ids/
%endif
%if 0%{?suse_version} < 1130
%exclude %{_libdir}/libvdpau.so
%exclude %{_libdir}/libvdpau.so.1*
%exclude %{_libdir}/vdpau/libvdpau_trace.so.1*
%endif

%files -n nvidia-computeG04
%defattr(-,root,root)
%dir %{_sysconfdir}/OpenCL
%dir %{_sysconfdir}/OpenCL/vendors
%config %{_sysconfdir}/OpenCL/vendors/nvidia.icd
%{_mandir}/man1/nvidia-cuda-mps-control.1.gz
%{_libdir}/libcuda.so*
%{_libdir}/libOpenCL.so*
%{_libdir}/libnvidia-ml.so*
%{_libdir}/libnvidia-of.so*
%{_libdir}/libnvidia-opencl.so*
%{_libdir}/libnvidia-fatbinaryloader.so*
%{_libdir}/libnvidia-ptxjitcompiler.so*
%{_bindir}/nvidia-smi
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-modprobe
%ifarch x86_64
%{_prefix}/lib/libcuda.so*
%{_prefix}/lib/libOpenCL.so*
%{_prefix}/lib/libnvidia-ml.so*
%{_prefix}/lib/libnvidia-of.so*
%{_prefix}/lib/libnvidia-opencl.so*
%{_prefix}/lib/libnvidia-fatbinaryloader.so*
%{_prefix}/lib/libnvidia-ptxjitcompiler.so*
%endif

%files -n nvidia-glG04
%defattr(-,root,root)
%dir /etc/vulkan
%dir /etc/vulkan/icd.d
%dir %{_datadir}/egl
%dir %{_datadir}/egl/egl_external_platform.d
%config /etc/vulkan/icd.d/nvidia_icd.json
%config %{_datadir}/egl/egl_external_platform.d/10_nvidia_wayland.json
%if 0%{?suse_version} >= 1330
%dir %{_datadir}/glvnd
%dir %{_datadir}/glvnd/egl_vendor.d
%config %{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%endif
%if 0%{?suse_version} > 1140
%if 0%{?suse_version} < 1330
%config %{_sysconfdir}/ld.so.conf.d/nvidia-gfxG04.conf
%endif
%endif
%if 0%{?suse_version} < 1330
%{_prefix}/X11R6/%{_lib}/libGL.so*
%{_prefix}/X11R6/%{_lib}/libGLX_nvidia.so*
%{_prefix}/X11R6/%{_lib}/libGLdispatch.so*
%{_prefix}/X11R6/%{_lib}/libEGL.so*
%{_prefix}/X11R6/%{_lib}/libGLESv1_CM.so*
%{_prefix}/X11R6/%{_lib}/libGLESv2.so*
%{_prefix}/X11R6/%{_lib}/libGLESv1_CM_nvidia.so*
%{_prefix}/X11R6/%{_lib}/libGLESv2_nvidia.so*
%{_prefix}/X11R6/%{_lib}/libOpenGL.so*
%else
%{_prefix}/%{_lib}/libGLX_nvidia.so*
%{_prefix}/%{_lib}/libEGL_nvidia.so*
%{_prefix}/%{_lib}/libGLESv1_CM_nvidia.so*
%{_prefix}/%{_lib}/libGLESv2_nvidia.so*
%endif
%{_libdir}/libnvidia-glcore.so*
%{_libdir}/libnvidia-ifr.so*
%{_libdir}/libnvidia-fbc.so*
%{_libdir}/libnvidia-egl-wayland.so*
%{_libdir}/libnvidia-gtk*
%{_libdir}/libnvidia-tls.so*
%{_libdir}/libnvidia-glsi.so*
%{_libdir}/libnvidia-eglcore.so*
%{_libdir}/libnvoptix.so*
%dir %{_libdir}/tls
%{_libdir}/tls/libnvidia-tls.so*
%{xmodulesdir}/extensions
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%ifarch x86_64
%if 0%{?suse_version} < 1330
%{_prefix}/X11R6/lib/libGL.so*
%{_prefix}/X11R6/lib/libGLX_nvidia.so*
%{_prefix}/X11R6/lib/libGLdispatch.so*
%{_prefix}/X11R6/lib/libEGL.so*
%{_prefix}/X11R6/lib/libGLESv1_CM.so*
%{_prefix}/X11R6/lib/libGLESv2.so*
%{_prefix}/X11R6/lib/libGLESv1_CM_nvidia.so*
%{_prefix}/X11R6/lib/libGLESv2_nvidia.so*
%{_prefix}/X11R6/lib/libOpenGL.so*
%else
%{_prefix}/lib/libGLX_nvidia.so*
%{_prefix}/lib/libEGL_nvidia.so*
%{_prefix}/lib/libGLESv1_CM_nvidia.so*
%{_prefix}/lib/libGLESv2_nvidia.so*
%endif
%{_prefix}/lib/libnvidia-glcore.so*
%{_prefix}/lib/libnvidia-ifr.so*
%{_prefix}/lib/libnvidia-eglcore.so*
%{_prefix}/lib/libnvidia-glsi.so*
%{_prefix}/lib/libnvidia-tls.so*
%dir %{_prefix}/lib/tls
%{_prefix}/lib/tls/libnvidia-tls.so*
%endif

%if 0%{?diagnostic}
%files -n nvidia-diagnosticG04
%defattr(-,root,root,-)
/usr/share/nvidia/diagnostic
%endif

%if 0%{?suse_version} < 1130

%files -n libvdpau1
%defattr(-,root,root)
%dir %{_libdir}/vdpau
/usr/bin/vdpauinfo
%{_libdir}/libvdpau.so.1*

%files -n libvdpau-devel
%defattr(-,root,root)
%doc %{_datadir}/doc/libvdpau
%dir %{_libdir}/vdpau
%{_includedir}/vdpau
%{_libdir}/libvdpau.so
%{_libdir}/pkgconfig/vdpau.pc

%files -n libvdpau_trace1
%defattr(-,root,root)
%dir %{_libdir}/vdpau
%{_libdir}/vdpau/libvdpau_trace.so.1*

%endif

%changelog
