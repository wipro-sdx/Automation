#!/usr/bin/python
import os
import csv


#filename = raw_input("Enter the input file name : ")
filename = "/var/lib/awx/projects/multivmosselection/input.csv"
if os.path.exists(filename):
    print "Given File exists... Processing it"
    inpfile = open (filename,'r')
    inpwriter = csv.reader(inpfile)
    inplist = list(inpwriter)
    i = 1
    row = len(open(filename).readlines())
    
    while i < row:

      servername = inplist[i][0]
      disksize = inplist[i][1]
      mem = inplist[i][2]
      cpu = inplist[i][3]
      ip = inplist[i][4]
      ops = inplist[i][5]
      cmd = 'ansible-playbook /var/lib/awx/projects/multivmosselection/multivmosselection.yml -i /var/lib/awx/projects/multivmosselection/hosts --extra-vars "servername=%s disksize=%s mem=%s cpu=%s ip=%s ops=%s"'%(servername,disksize,mem,cpu,ip,ops)
      #cmd = 'ansible-playbook /var/lib/awx/projects/cobbler/cobbler.yml -i /var/lib/awx/projects/cobbler/hosts --extra-vars "systemname=%s profile=%s interface=%s mac=%s ipaddr=%s netmask=%s gw=%s powaddr=%s powuser=%s powpass=%s"'%(systemname,profile,interface,mac,ipaddr,netmask,gw,powaddr,powuser,powpass)
      os.system(cmd)
      i = i + 1
else:
  print "File doesn't exit"
