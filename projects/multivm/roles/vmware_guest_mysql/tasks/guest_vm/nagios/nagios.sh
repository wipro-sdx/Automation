#adding nagios user.
useradd nagios
echo "nagios" |passwd nagios --stdin

#install packages

yum install -y gcc glibc glibc-common openssl openssl-devel perl wget gd gd-devel make net-snmp

#coping packages
#mkdir /root/nagios
#scp -r root@192.168.106.101:/root/nagios/* /root/nagios/
#useradd nagios
#echo "nagios" |passwd nagios --stdin

#installing nagios plugins
cd /root/nagios/nagios-plugins-2.2.1/

./configure 

make

make install

chown nagios.nagios /usr/local/nagios

chown -R nagios.nagios /usr/local/nagios/libexec

cd

# Installing xinetd
yum install -y xinetd


#instaling NRPE
cd

cd /root/nagios/nrpe-nrpe-3.2.1/

./configure --enable-command-args

make all

make install

make install-config

echo 'nrpe    5666/tcp' >> /etc/services

#Starting NRPE Services
make install-init
systemctl enable nrpe.service

firewall-cmd --zone=public --add-port=5666/tcp
firewall-cmd --zone=public --add-port=5666/tcp --permanent

cp /usr/local/nagios/etc/nrpe.cfg /usr/local/nagios/etc/nrpe.cfg.bkp

sed -i '/^allowed_hosts=/s/$/,172.17.65.214/' /usr/local/nagios/etc/nrpe.cfg
sed -i 's/^dont_blame_nrpe=.*/dont_blame_nrpe=1/g' /usr/local/nagios/etc/nrpe.cfg


systemctl start nrpe.service
systemctl stop nrpe.service
systemctl restart nrpe.service
systemctl status nrpe.service

/usr/local/nagios/libexec/check_nrpe -H 127.0.0.1

