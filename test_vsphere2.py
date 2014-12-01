#!/usr/bin/python
"""kvirt sample test against portal"""

import sys
from portal.vsphere2 import Vsphere
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'basic6'
name1 = 'portal'
name2 = 'prout'

profile = Profile.objects.get(name=profile)
virtualprovider = profile.virtualprovider
vchost, vcport, vcuser, vcpassword, dc, clu  = virtualprovider.host, virtualprovider.port, virtualprovider.user, virtualprovider.password, virtualprovider.dc, virtualprovider.clu
clu, numcpu, numinterfaces, netinterface, diskthin1, disksize1, diskinterface,memory, guestid, net1, net2, net3, net4, diskthin2, disksize2,vnc =  profile.clu, profile.numcpu, profile.numinterfaces, profile.netinterface, profile.diskthin1, profile.disksize1, profile.diskinterface,profile.memory, profile.guestid, profile.net1, profile.net2, profile.net3, profile.net4, profile.diskthin2, profile.disksize2, profile.vnc
datacenter = virtualprovider.datacenter

v   = Vsphere(vchost,vcport,vcuser,vcpassword, dc, clu)
print v.gettemplates()
sys.exit(0)
print v.getisos()
print v.getstorage()
storagedomain = v.beststorage(datacenter)
print storagedomain
print v.allvms()
print v.status(name1)
print v.console(name1)
print v.getmacs(name1)
#print v.create(name2, clu, numcpu, numinterfaces, netinterface, diskthin1, disksize1, diskinterface,memory, storagedomain, guestid, net1, net2=net2, net3=net3, net4=net4, iso=iso, diskthin2=diskthin2, disksize2=disksize2,vnc=vnc)
#print v.start(name2)
#print v.remove(name2)
sys.exit(0)
