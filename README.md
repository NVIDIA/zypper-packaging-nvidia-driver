# zypper packaging nvidia driver

[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT-license)
[![Contributing](https://img.shields.io/badge/Contributing-Developer%20Certificate%20of%20Origin-violet)](https://developercertificate.org)

## Overview

Packaging templates for `zypper` based Linux distros to build NVIDIA driver packages.

The `main` branch contains this README. The `.spec`, `.sh`, and etc. files can be found in the appropriate [gfxG04](../../tree/gfxG04) and [gfxG05](../../tree/gfxG05) branches.

## Table of Contents

- [Overview](#Overview)
- [Deliverables](#Deliverables)
- [Prerequisites](#Prerequisites)
  * [Clone this git repository](#Clone-this-git-repository)
  * [Install build dependencies](#Install-build-dependencies)
- [Related](#Related)
  * [Fabric Manager](#Fabric-Manager)
  * [NSCQ library](#NSCQ-library)
- [See also](#See-also)
  * [Ubuntu driver](#Ubuntu-driver)
  * [RHEL driver](#RHEL-driver)
- [Contributing](#Contributing)


## Deliverables

This repo contains the `.spec` file used to build the following **RPM** packages:

> _note:_ upgrading between gfxG0[0-9] flavors requires uninstall

* **openSUSE 15** or **SLES 15**: [gfxG05](https://build.opensuse.org/package/show/X11:Drivers:Video/nvidia-gfxG05)
 ```shell
 - nvidia-computeG05-${version}-${rel}.${arch}.rpm
 - nvidia-gfxG05-kmp-azure-${version}_k${kernel}-${rel}.${arch}.rpm
 - nvidia-gfxG05-kmp-default-${version}_k${kernel}-${rel}.${arch}.rpm
 - nvidia-glG05-${version}-${rel}.${arch}.rpm
 - x11-video-nvidiaG05-${version}-${rel}.${arch}.rpm
 ```

 > _note:_ Azure package only builds on `SLES`

* **openSUSE 12** or **SLES 12**: [gfxG04](https://build.opensuse.org/package/show/X11:Drivers:Video/nvidia-gfxG04)
 ```shell
 - nvidia-computeG04-${version}-${rel}.${arch}.rpm
 - nvidia-gfxG04-kmp-default-${version}_k${kernel}-${rel}.${arch}.rpm
 - nvidia-glG04-${version}-${rel}.${arch}.rpm
 - x11-video-nvidiaG04-${version}-${rel}.${arch}.rpm
 ```

## Prerequisites

### Clone this git repository:

Supported branches: `gfxG04` & `gfxG05`

```shell
git clone -b ${branch} https://github.com/NVIDIA/zypper-packaging-nvidia-driver
> ex: git clone -b gfxG05 https://github.com/NVIDIA/zypper-packaging-nvidia-driver
```

### Install build dependencies

```shell
# Basics
zypper install gcc-c++ module-init-tools pkgconfig
# gfxG05
zypper install kernel-source kernel-syms kernel-syms-azure
# gfxG04
zypper install bison flex kernel-source kernel-syms
# X.org utilities
zypper install xorg-x11-devel
# Misc
zypper install doxygen graphviz texlive update-desktop-files
# Packaging
zypper install rpm-build
```

## Related

### Fabric Manager

- fabricmanager
  * [https://github.com/NVIDIA/yum-packaging-fabric-manager](https://github.com/NVIDIA/yum-packaging-fabric-manager)

### NSCQ library

- libnvidia-nscq
  * [https://github.com/NVIDIA/yum-packaging-libnvidia-nscq](https://github.com/NVIDIA/yum-packaging-libnvidia-nscq)


## See also

- X11:Drivers:Video
  * [https://build.opensuse.org/project/show/X11:Drivers:Video](https://build.opensuse.org/project/show/X11:Drivers:Video)

### Ubuntu driver

  * [https://github.com/NVIDIA/ubuntu-packaging-nvidia-driver](https://github.com/NVIDIA/ubuntu-packaging-nvidia-driver)

### RHEL driver

  * [https://github.com/NVIDIA/yum-packaging-nvidia-driver](https://github.com/NVIDIA/yum-packaging-nvidia-driver)


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
