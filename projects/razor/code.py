#!/usr/bin/python
import os
import csv


#filename = raw_input("Enter the input file name : ")
filename = "/var/lib/awx/projects/razor/input.csv"
if os.path.exists(filename):
    print "Given File exists... Processing it"
    inpfile = open (filename,'r')
    inpwriter = csv.reader(inpfile)
    inplist = list(inpwriter)
    i = 1
    row = len(open(filename).readlines())
    
    while i < row:

      tagname = inplist[i][0]
      mac = inplist[i][1]
      policyname = inplist[i][2]
      servername = inplist[i][3]
      cmd = 'ansible-playbook /var/lib/awx/projects/razor/razor.yml -i /var/lib/awx/projects/razor/hosts --extra-vars "tagname=%s mac=%s policyname=%s servername=%s"'%(tagname,mac,policyname,servername)
      #cmd = 'ansible-playbook /var/lib/awx/projects/cobbler/cobbler.yml -i /var/lib/awx/projects/cobbler/hosts --extra-vars "systemname=%s profile=%s interface=%s mac=%s ipaddr=%s netmask=%s gw=%s powaddr=%s powuser=%s powpass=%s"'%(systemname,profile,interface,mac,ipaddr,netmask,gw,powaddr,powuser,powpass)
      os.system(cmd)
      i = i + 1
else:
  print "File doesn't exit"
