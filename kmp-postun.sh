flavor=%1
if [ "$1" = 0 ] ; then
    # Avoid accidental removal of G<n+1> alternative (bnc#802624)
    if [ ! -f /usr/lib/nvidia/alternate-install-present-$flavor ];  then
	%{_sbindir}/update-alternatives --remove alternate-install-present /usr/lib/nvidia/alternate-install-present-$flavor
    fi
    # cleanup of bnc# 1000625
    rm -f /etc/tmpfiles.d/nvidia-hack.conf
fi
