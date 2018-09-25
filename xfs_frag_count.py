#!/usr/bin/env python

import sys
try:
    from subprocess import check_output
except ImportError:
    print '0 XFS_fragmentation - check_output function not found'
    sys.exit(0)

try:
    devnull = open('/dev/null', 'w')
    xfs_libvirt_device = check_output(
        "mount -t xfs | grep 'libvirt' | awk {'print $1'} | tr -d '\n'",
        shell=True, stderr=devnull)
except:
    print '0 XFS_fragmentation - mount cmd failed'
    devnull.close()
    sys.exit(0)

try:
    xfs_frag_cmd = 'xfs_db -r %s -c frag' % xfs_libvirt_device
    xfs_frag = check_output(
        xfs_frag_cmd + 
        " | grep 'factor' | awk {'print $7'} | tr -d '%\n'", 
        shell=True, stderr=devnull)
    xfs_frag_value = float(xfs_frag)
except:
    print '0 XFS_fragmentation - xfs_db cmd failed'
    devnull.close()
    sys.exit(0)

devnull.close()

crit_treshold = 99.99
warn_treshold = 95.0

crit_msg = ('2 XFS_fragmentation percent=%s;%s;%s FragCounts - '
'%s percent fragmentation') \
% (xfs_frag_value, warn_treshold, crit_treshold, xfs_frag_value)

warn_msg = ('1 XFS_fragmentation percent=%s;%s;%s FragCounts - '
'%s percent fragmentation') \
% (xfs_frag_value, warn_treshold, crit_treshold, xfs_frag_value)

ok_msg = ('0 XFS_fragmentation percent=%s;%s;%s FragCounts - '
'%s percent fragmentation') \
% (xfs_frag_value, warn_treshold, crit_treshold, xfs_frag_value)

if xfs_frag_value >= crit_treshold:
    print crit_msg
elif xfs_frag_value >= warn_treshold:
    print warn_msg
else:
    print ok_msg