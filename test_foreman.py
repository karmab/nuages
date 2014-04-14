#!/usr/bin/python
"""foreman sample test against portal"""

import sys
from portal.foreman import Foreman
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'basic6'
#name='k1.lab'
environment='production'
classname = 'test2'

profile = Profile.objects.get(name=profile)
foremanprovider = profile.foremanprovider
foremanhost, foremanport, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port, foremanprovider.user, foremanprovider.password
f = Foreman(foremanhost,foremanport,foremanuser, foremanpassword)
#print f.hostgroups(environment)
classes = f.classes(environment)
print classes
#for classe in classes:
#    print f.classinfo(classe)
#print f.override('test2','testdir')
sys.exit(0)
