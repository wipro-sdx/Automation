#!usr/bin/env python
import os
import csv
import sys

#This version is added with Virtual IP and Self IP configuration

host_file = open ('host.csv','r')
host_writer = csv.reader(host_file)
host_list = list(host_writer)
host_count = len(host_list)
print "Total F5_load balancers to be configured: ", host_count-1
count = 1
while count < host_count:

 #Node creation
 print "Server being configured: ", host_list[count]
 node_file = open ('node.csv','r')
 node_writer = csv.reader(node_file)
 node_list = list(node_writer)
 i = 1
 row = len(open('node.csv').readlines())
 #print row
 while i < row:
   node_name = node_list[i][0]
   addr = node_list[i][1]
   node_state = node_list[i][2]
   cmd = 'ansible-playbook f5_node_create.yml --extra-vars "node_name=%s addr=%s node_state=%s f5_ip=%s" -i hosts'%(node_name,addr,node_state,host_list[count])
   #print cmd
   os.system(cmd)
   i = i + 1

 #NTP_DNS Config

 inp_file = open ('ntp_dns.csv','r')
 inp_writer = csv.reader(inp_file)
 inp_list = list(inp_writer)
 j = 1
 row_count = len(open('ntp_dns.csv').readlines())
 #print row
 while j < row_count:

   if (inp_list[j][0] == 'ntp'):
     ipaddr = inp_list[j][1]
     cmd = 'ansible-playbook f5_ntp.yml --extra-vars "server_addr=%s f5_ip=%s" -i hosts'%(ipaddr,host_list[count])
   elif (inp_list[j][0] == 'dns'):
     ipaddr = inp_list[j][1]
     cmd = 'ansible-playbook f5_dns.yml --extra-vars "server_addr=%s f5_ip=%s" -i hosts'%(ipaddr,host_list[count])
   #print cmd
   os.system(cmd)
   j = j + 1

 #POOL Config

 pool_file = open ('pool.csv','r')
 pool_writer = csv.reader(pool_file)
 pool_list = list(pool_writer)
 k = 1
 poolrow_count = len(open('pool.csv').readlines())
 #print row
 while k < poolrow_count:
   pool_name = pool_list[k][0]
   lbmethod_name = pool_list[k][1]
   cmd = 'ansible-playbook f5_pool_create.yml --extra-vars "pool_name=%s lb_name=%s f5_ip=%s" -i hosts'%(pool_name,lbmethod_name,host_list[count])
   os.system(cmd)
   #print cmd
   k = k + 1

 #POOL Member Config

 pool_mem_file = open ('pool_member.csv','r')
 pool_mem_writer = csv.reader(pool_mem_file)
 pool_mem_list = list(pool_mem_writer)
 l = 1
 mem_count = len(open('pool_member.csv').readlines())
 #print row
 while l < mem_count:
   poolname = pool_mem_list[l][0]
   server_ip = pool_mem_list[l][1]
   port = pool_mem_list[l][2]
   cmd = 'ansible-playbook f5_pool_member.yml --extra-vars "pool_name=%s server_ip=%s port_num=%d f5_ip=%s" -i hosts'%(poolname,server_ip,int(port),host_list[count])
   os.system(cmd)
   #print cmd
   l = l + 1

 #Virtual IP Config

 vip_file = open ('vip.csv','r')
 vip_writer = csv.reader(vip_file)
 vip_list = list(vip_writer)
 v = 1
 vip_count = len(open('vip.csv').readlines())
 #print row
 while v < vip_count:
   vip_name = vip_list[v][0]
   vip_ip = vip_list[v][1]
   port = vip_list[v][2]
   pool_name = vip_list[v][3]
   profile = vip_list[v][4]
   cmd = 'ansible-playbook f5_virtualserver.yml --extra-vars "vip_name=%s dest_ip=%s port_num=%d pool_name=%s profile=%s f5_ip=%s" -i hosts'%(vip_name,vip_ip,int(port),pool_name,profile,host_list[count])
   os.system(cmd)
   #print cmd
   v = v + 1

 #Self IP Config

 sip_file = open ('selfip.csv','r')
 sip_writer = csv.reader(sip_file)
 sip_list = list(sip_writer)
 s = 1
 sip_count = len(open('selfip.csv').readlines())
 #print row
 while s < sip_count:
   sip_name = sip_list[s][0]
   sip_ip = sip_list[s][1]
   sip_mask = sip_list[s][2]
   sip_vlan = sip_list[s][3]
   cmd = 'ansible-playbook f5_selfip.yml --extra-vars "sip_name=%s sip_ip=%s sip_mask=%s sip_vlan=%s f5_ip=%s" -i hosts'%(sip_name,sip_ip,sip_mask,sip_vlan,host_list[count])
   os.system(cmd)
   #print cmd
   s = s + 1

 count = count + 1 
