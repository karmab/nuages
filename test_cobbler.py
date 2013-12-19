#!/usr/bin/python
"""cobbler sample test against portal"""

import sys
from portal.cobbler import Cobbler
from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profile = 'lab6'

profile = Profile.objects.get(name=profile)
cobblerhost, cobbleruser, cobblerpassword = cobblerprovider.host, cobblerprovider.user, cobblerprovider.password
c = Cobbler(cobblerhost,cobbleruser, cobblerpassword)
print c.checkprofile(profile)
sys.exit(0)
