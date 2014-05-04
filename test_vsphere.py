#!/usr/bin/python
"""vsphere sample test against portal"""

import sys
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *
from django.conf import settings

#profile = 'vsphere6'
name1 = 'kfailure'
name2 = 'prout'

#profile = Profile.objects.get(name=profile)
virtualprovider = VirtualProvider.objects.get(name='amsterdam')
#clu, numcpu, numinterfaces, netinterface, diskthin1, disksize1, diskinterface,memory, guestid, net1, net2, net3, net4, diskthin2, disksize2,vnc =  profile.clu, profile.numcpu, profile.numinterfaces, profile.netinterface, profile.diskthin1, profile.disksize1, profile.diskinterface,profile.memory, profile.guestid, profile.net1, profile.net2, profile.net3, profile.net4, profile.diskthin2, profile.disksize2, profile.vnc
datacenter = virtualprovider.datacenter

storagecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (settings.PWD, 'getstorage', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu )
#storageinfo = os.popen(storagecommand).read()
#storageinfo = ast.literal_eval(storageinfo)
#print storageinfo

isoscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (settings.PWD, 'getisos', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu )
#isosinfo = os.popen(isoscommand).read()
#isosinfo = ast.literal_eval(isosinfo)
#print isosinfo

allvmscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s " % (settings.PWD, 'allvms', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu )
#allvmsinfo = os.popen(allvmscommand).read()
#allvmsinfo = ast.literal_eval(allvmsinfo)
#print allvmsinfo

html5command = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s %s %s" % (settings.PWD, 'html5console', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu, name1, virtualprovider.fqdn, virtualprovider.sha1  )
html5info = os.popen(html5command).read()
html5info = ast.literal_eval(html5info)
print html5info
