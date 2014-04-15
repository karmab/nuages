#!/usr/bin/python
"""foreman sample test against portal"""

import sys
from portal.foreman import Foreman
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'basic6'
name1='k1000'
name2='k8000'
environment='production'
classname = 'test2'
ip1="192.168.8.90"
dns="ib"
hostgroup="default"
parameters="testdir=/root/megafrout"

profile = Profile.objects.get(name=profile)
foremanprovider = profile.foremanprovider
foremanhost, foremanport, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port, foremanprovider.user, foremanprovider.password
f = Foreman(foremanhost,foremanport,foremanuser, foremanpassword)
#print f.exists(name1,dns)
#print f.delete(name1,dns)
#print f.hostgroups(environment)
#classes = f.classes(environment)
#print classes
#for classe in classes:
#    print f.classinfo(classe)
#
#print f.create(name=name2, dns=dns, ip=ip1, hostgroup=hostgroup)
#print f.override('test2','testdir')
print f.addparameters(name2,dns,parameters)
sys.exit(0)
