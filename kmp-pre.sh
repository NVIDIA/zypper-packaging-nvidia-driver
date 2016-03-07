# get rid of old kernel modules and weak-updates(2) symlinks (bnc#969763)
flavor=%1
rm -f /lib/modules/*-$flavor/updates/nvidia*.ko
find  /lib/modules/*-$flavor/weak-updates -name "nvidia*.ko" -delete || true

if [ -x /usr/bin/nvidia-uninstall ]; then
    /usr/bin/nvidia-uninstall -s || :
fi;
