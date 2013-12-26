#!/usr/bin/python
"""kvirt sample test against portal"""

import sys
from portal.ovirt import Ovirt
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'basic6'
name1 = 'portal'
name2 = 'prout'

profile = Profile.objects.get(name=profile)
virtualprovider = profile.virtualprovider
ohost, oport, ouser, opassword, ossl = virtualprovider.host, virtualprovider.port, virtualprovider.user, virtualprovider.password, virtualprovider.ssl
clu, numcpu, numinterfaces, netinterface, diskformat1, disksize1, diskinterface,memory, guestid, net1, net2, net3, net4, diskformat2, disksize2,vnc =  profile.clu, profile.numcpu, profile.numinterfaces, profile.netinterface, profile.diskformat1, profile.disksize1, profile.diskinterface,profile.memory, profile.guestid, profile.net1, profile.net2, profile.net3, profile.net4, profile.diskformat2, profile.disksize2, profile.vnc
datacenter = virtualprovider.datacenter


o = Ovirt(ohost, oport, ouser, opassword, ossl)
print o.getisos()
print o.getstorage()
storagedomain = o.beststorage(datacenter)
print storagedomain
print o.allvms()
print o.status(name1)
print o.console(name1)
print o.getmacs(name1)
#print o.create(name2, clu, numcpu, numinterfaces, netinterface, diskformat1, disksize1, diskinterface,memory, storagedomain, guestid, net1, net2=net2, net3=net3, net4=net4, iso=iso, diskformat2=diskformat2, disksize2=disksize2,vnc=vnc)
#print o.start(name2)
#print o.remove(name2)
sys.exit(0)
