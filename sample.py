#!/usr/bin/python
"""example of how to interact with django db"""

from django.core.management import setup_environ
import nuages.settings
setup_environ(nuages.settings)
from portal.models import *

profiles=Profile.objects.all()
for p in profiles:
            print p.name,p.cmdline,p.nextserver
            #        if p.name.startswith('des') or p.name.startswith('pre'):
            #               p.nextserver = '192.168.136.33'
            #       else:
            #               p.nextserver = '192.168.133.220'
            #       p.cmdline = p.cmdline.replace('location', 'repo')
            #       p.save()

