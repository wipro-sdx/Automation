#!usr/bin/env python
import os
import csv

#Feature Config

feature_file = open ('feature.csv','r')
feature_writer = csv.reader(feature_file)
feature_list = list(feature_writer)
fi = 1
frow = len(open('feature.csv').readlines())
#print row
while fi < frow:
  fname = feature_list[fi][0]
  faction = feature_list[fi][1]
  cmd = 'ansible-playbook -v nxos_config_feature_prompt.yml --extra-vars "fname=%s faction=%s" -i hosts'%(fname,faction)
  #print cmd
  os.system(cmd)
  fi = fi + 1

#Interface Configuration

interface_file = open ('interface.csv','r')
interface_writer = csv.reader(interface_file)
interface_list = list(interface_writer)
interface_count = 1
interface_row = len(open('interface.csv').readlines())
#print row
while interface_count < interface_row:
  interface = interface_list[interface_count][0]
  desc = interface_list[interface_count][1]
  mode = interface_list[interface_count][2]
  ip_addr = interface_list[interface_count][3]
  mask = interface_list[interface_count][4]
  cmd = 'ansible-playbook -v nxos_config_interface.yml --extra-vars "interface=%s desc=%s mode=%s ip_addr=%s addr_mask=%d" -i hosts'%(interface,desc,mode,ip_addr,int(mask))
  #print cmd
  os.system(cmd)
  interface_count = interface_count + 1



#OSPF Provisioning

ospf_file = open ('ospf.csv','r')
ospf_writer = csv.reader(ospf_file)
ospf_list = list(ospf_writer)
oi = 1
ospf_row = len(open('ospf.csv').readlines())
while oi < ospf_row:
  ospf_pid = ospf_list[oi][0]
  ospf_area = ospf_list[oi][1]
  ospf_cost = ospf_list[oi][2]
  ospf_interface = ospf_list[oi][3]
  cmd = 'ansible-playbook -v nxos_ospf_prompt.yml --extra-vars "pid=%d area=%d cost=%d intf='"'%s'"'" -i hosts'%(int(ospf_pid),int(ospf_area),int(ospf_cost),ospf_interface)
  #print cmd
  os.system(cmd)
  oi = oi + 1

#Static Route Provisioning

sroute_file = open ('static_route.csv','r')
sroute_writer = csv.reader(sroute_file)
sroute_list = list(sroute_writer)
sroute_count = 1
sroute_row = len(open('static_route.csv').readlines())
while sroute_count < sroute_row:
  sr_prefix = sroute_list[sroute_count][0]
  sr_nexthop = sroute_list[sroute_count][1]
  cmd = 'ansible-playbook -v nxos_stroute_prompt.yml --extra-vars "prefix=%s nexthop=%s" -i hosts'%(sr_prefix,sr_nexthop)
  #print cmd
  os.system(cmd)
  sroute_count = sroute_count + 1

#VLAN Creation/Deletion

vlan_file = open ('vlan.csv','r')
vlan_writer = csv.reader(vlan_file)
vlan_list = list(vlan_writer)
vlan_count = 1
vlan_row = len(open('vlan.csv').readlines())
while vlan_count < vlan_row:
  if (vlan_list[vlan_count][0] == 'create'):
    vlan_id = vlan_list[vlan_count][1]
    vlan_state = vlan_list[vlan_count][2]
    vlan_name = vlan_list[vlan_count][3]
    cmd = 'ansible-playbook -v nxos_vlan_creation.yml --extra-vars "vlan_id=%d state=%s vlan_name=%s" -i hosts'%(int(vlan_id),vlan_state,vlan_name)
    os.system(cmd)
    #print cmd
  elif (vlan_list[vlan_count][0] == 'delete'):
    vlan_id = vlan_list[vlan_count][1]
    cmd = 'ansible-playbook -v nxos_vlan_deletion.yml --extra-vars "vlan_id=%d" -i hosts'%(int(vlan_id))
    #print cmd
    os.system(cmd)
  vlan_count = vlan_count + 1
 
