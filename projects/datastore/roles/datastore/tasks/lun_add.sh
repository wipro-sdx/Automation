#!/bin/sh
esxcfg-rescan -A
ls -ltr /vmfs/devices/disks/ | awk {'print $11'} > /tmp/afterscan
lun=`diff /tmp/afterscan /tmp/beforescan |grep -e -naa | cut -c 2-`
partedUtil set "/vmfs/devices/disks/$lun" "1 128 500000 251 0"
echo -e "o\nn\np\nd\n1\n\n\nt\nfb\nw" | fdisk /vmfs/devices/disks/$lun
vmkfstools -C vmfs5 -b 1m /vmfs/devices/disks/$lun:1
