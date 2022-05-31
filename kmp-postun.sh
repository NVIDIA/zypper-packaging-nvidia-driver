flavor=%1
if [ "$1" = 0 ] ; then
    # Avoid accidental removal of G<n+1> alternative (bnc#802624)
    if [ ! -f /usr/lib/nvidia/alternate-install-present-$flavor ];  then
	%{_sbindir}/update-alternatives --remove alternate-install-present /usr/lib/nvidia/alternate-install-present-$flavor
    fi
    # cleanup of bnc# 1000625
    rm -f /usr/lib/tmpfiles.d/nvidia-logind-acl-trick-G05.conf

    # Remove old .ko files that the %ghost didn't clean up
    # Runs ONLY during uninstall due to ordering (running during upgrade would remove the just-installed .ko files)
    rm /lib/modules/*/updates/nvidia*.ko
fi
