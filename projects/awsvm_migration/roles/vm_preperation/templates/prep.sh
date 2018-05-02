df -h | grep -i loop | awk '{print $6}'| xargs umount
ls -l /etc/sysconfig/network-scripts/ifcfg-e* | awk '{print $9}' > /tmp/list 
for i in `cat /tmp/list`; do  sed -i 's/BOOTPROTO=.*/BOOTPROTO=dhcp/' $i; sed -i 's/IPADDR=.*/IPADDR=/' $i; sed -i 's/NETMASK=.*/NETMASK=/' $i; sed -i 's/GATEWAY=.*/GATEWAY=/' $i; done
shutdown -h +1 "Server is going down for Migration. Please save your work."
