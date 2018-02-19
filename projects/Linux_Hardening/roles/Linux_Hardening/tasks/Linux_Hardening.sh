#Disable X Windows Startup
systemctl set-default multi-user.target

#Restrict at and cron to Authorised Users
echo root > /etc/cron.allow
echo root > /etc/at.allow
rm -f /etc/at.deny /etc/cron.deny

#Remove Obsolete Services
yum erase xinetd telnet-server rsh-server telnet rsh ypbind ypserv tfsp-server bind vsfptd dovercot squid net-snmpd talk-erver talk

#Disable kernel dump service
systemctl disable kdump.service
systemctl mask kdump.service

#Network Time Protocol
systemctl enable chronyd.service

#Allow SSH server to listen on TCP 2222
yum install policycoreutils-python -y
semanage port -a -t ssh_port_t 2222 -p tcp

#Disable Ctrl-Alt-Del Reboot Activation
systemctl mask ctrl-alt-del.target

#Multiple Console Screens
yum install screen -y

#Verify All Account Password Hashes are Shadowed
cut -d: -f2 /etc/passwd|uniq

#Log Failed Login Attemps
echo "FAILLOG_ENAB yes" >> /etc/login.defs
echo "FAIL_DELAY 4" >> /etc/login.defs

# Secure Pasword Policy
echo "PASS_MAX_DAYS 60" >> /etc/login.defs
echo "PASS_MIN_DAYS 1" >> /etc/login.defs
echo "PASS_MIN_LEN 14" >> /etc/login.defs
echo "PASS_WARN_AGE 14" >> /etc/login.defs

#Set Account Expiration Following Inactivity
echo "INACTIVE=0" >>  /etc/default/useradd

#Prevent Log In to Accounts With Empty Password
sed -i 's/\<nullok\>//g' /etc/pam.d/system-auth /etc/pam.d/password-auth

#Disable Direct root Login
echo > /etc/securetty

#Set the SELinux State 
#Edit the /etc/selinux/config file to set the SELINUX parameter: SELINUX=enforcing
sed -i 's/SELINUX=disabled/SELINUX=enforcing/' /etc/selinux/config
#sed -i 's/SELINUX=permissive/SELINUX=enforcing/' /etc/selinux/config

#Configure rsyslog
#Install the rsyslog package  
yum install rsyslog -y

#Enable Rsyslog
systemctl enable rsyslog.service
systemctl start rsyslog.service

#Lock Inactive User Accounts
useradd -D -f 35

#Prevent Users Mounting USB Storage
echo "blacklist usb-storage" >> /etc/modprobe.d/hardening.conf
echo "blacklist firewire-core" >> /etc/modprobe.d/hardening.conf
echo "install usb-storage" >> /etc/modprobe.d/hardening.conf

#Disable unused services
#yum install telnet -y 
#systemctl stop telnet
#systemctl disable telnet

