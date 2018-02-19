#!/bin/sh
ls -ltr /vmfs/devices/disks/ | awk {'print $11'} > /tmp/beforescan
