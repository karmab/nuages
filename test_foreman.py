#!/usr/bin/python
"""foreman sample test against portal"""

import sys
from portal.foreman import Foreman
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'lab6'
name='k1.lab'
environment='production'

profile = Profile.objects.get(name=profile)
foremanprovider = profile.foremanprovider
foremanhost, foremanport, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port, foremanprovider.user, foremanprovider.password
f = Foreman(foremanhost,foremanport,foremanuser, foremanpassword)
print f.hostgroups(environment)
print f.exists(name)
sys.exit(0)
