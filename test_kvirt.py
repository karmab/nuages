#!/usr/bin/python
"""kvirt sample test against portal"""

import sys
from portal.kvirt import Kvirt
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'lab6iso'
name1 = 'ktool'
name2 = 'prout'
iso='/var/lib/libvirt/images/rhel-server-6.4-x86_64-dvd.iso'

profile = Profile.objects.get(name=profile)
virtualprovider = profile.virtualprovider
host,port,user = virtualprovider.host, virtualprovider.port, virtualprovider.user
clu, numcpu, numinterfaces, netinterface, diskthin1, disksize1, diskinterface,memory, guestid, net1, net2, net3, net4, diskthin2, disksize2,vnc =  profile.clu, profile.numcpu, profile.numinterfaces, profile.netinterface, profile.diskthin1, profile.disksize1, profile.diskinterface,profile.memory, profile.guestid, profile.net1, profile.net2, profile.net3, profile.net4, profile.diskthin2, profile.disksize2, profile.vnc

k = Kvirt(host,port,user)
print k.getisos()
print k.getstorage()
storagedomain = k.beststorage()
print storagedomain
print k.allvms()
print k.status(name1)
print k.console(name1)
print k.getmacs(name1)
print k.create(name2, clu, numcpu, numinterfaces, netinterface, diskthin1, disksize1, diskinterface,memory, storagedomain, guestid, net1, net2=net2, net3=net3, net4=net4, iso=iso, diskthin2=diskthin2, disksize2=disksize2,vnc=vnc)
print k.start(name2)
#print k.remove(name2)
sys.exit(0)
