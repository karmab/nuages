#-*- coding: utf-8 -*-
import os 
from django.forms import ModelForm
from portal.models import *
from django.contrib.auth.models import User,Group
from django.db.models import Q

class VMForm(ModelForm):
	def __init__(self, user, *args, **kwargs):
        	super(VMForm, self).__init__(*args, **kwargs)
		username	  = User.objects.filter(username=user)[0]
		if username.is_staff:
			return
		groups		  = username.groups
	    	usergroups=[]
	    	for g in groups.values():
			usergroups.append(g['id'])
		if len(usergroups) == 0:
                	query=Q(groups=None)
            	else:
                	query=Q(groups=None)|Q(groups=usergroups[0])
                	for group in usergroups[1:]:
                        	query=query|Q(groups=group)
                query=Profile.objects.filter(query)
        	self.fields['profile'].queryset = query
	class Meta:
		model = VM
		fields = ['name', 'physical', 'ipilo', 'ipoa', 'ip1','mac1', 'ip2', 'mac2', 'ip3', 'mac3', 'ip4', 'mac4', 'iso', 'virtualprovider', 'cobblerprovider', 'foremanprovider', 'hostgroup' , 'profile', 'puppetclasses', 'parameters']
		

class StorageForm(ModelForm):
	class Meta:
		model = Storage
