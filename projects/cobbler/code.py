#!usr/bin/env python
import os
import csv


#filename = raw_input("Enter the input file name : ")
filename = "/var/lib/awx/projects/cobbler/input.csv"
if os.path.exists(filename):
    print "Given File exists... Processing it"
    inpfile = open (filename,'r')
    inpwriter = csv.reader(inpfile)
    inplist = list(inpwriter)
    i = 1
    row = len(open(filename).readlines())
    
    while i < row:

      systemname = inplist[i][0]
      profile = inplist[i][1]
      interface = inplist[i][2]
      mac = inplist[i][3]
      ipaddr = inplist[i][4]
      netmask = inplist[i][5]
      gw = inplist[i][6]
      powaddr = inplist[i][7]
      powuser = inplist[i][8]
      powpass = inplist[i][9]
      cmd = 'ansible-playbook /var/lib/awx/projects/cobbler/cobbler.yml -i /var/lib/awx/projects/cobbler/hosts --extra-vars "systemname=%s profile=%s interface=%s mac=%s ipaddr=%s netmask=%s gw=%s powaddr=%s powuser=%s powpass=%s"'%(systemname,profile,interface,mac,ipaddr,netmask,gw,powaddr,powuser,powpass)
      print cmd
      os.system(cmd)
      i = i + 1
else:
  print "File doesn't exit"
