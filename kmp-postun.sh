flavor=%1
if [ "$1" = 0 ] ; then
    # Avoid accidental removal of G<n+1> alternative (bnc#802624)
    if [ ! -f /usr/lib/nvidia/alternate-install-present-$flavor ];  then
	%{_sbindir}/update-alternatives --remove alternate-install-present /usr/lib/nvidia/alternate-install-present-$flavor
    fi
    # cleanup of bnc# 1000625
    rm -f /usr/lib/tmpfiles.d/nvidia-logind-acl-trick-G05.conf
fi

# Remove old .ko files that the %ghost didn't clean up
# Runs regardless of upgrade or uninstall ($1 = 0 or $1 = 1)
rm /lib/modules/*/updates/nvidia*.ko
