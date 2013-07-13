#-*- coding: utf-8 -*-
import os 
from django.forms import ModelForm
from portal.models import VM,Storage,Oracle,Apache,Rac,Sap,Weblogic,Partitioning,Profile
from django.contrib.auth.models import User,Group
from django.db.models import Q

class VMForm(ModelForm):
	def __init__(self, user, *args, **kwargs):
        	super(VMForm, self).__init__(*args, **kwargs)
		username	  = User.objects.filter(username=user)[0]
		groups		  = username.groups
	    	usergroups=[]
	    	for g in groups.values():
			usergroups.append(g['id'])
            	profiles=[]
	    	allprofiles=Profile.objects.all()
	    	for p in allprofiles:
			found = False
			profilegroup=p.groups.values()
			if len(profilegroup) == 0:
				profiles.append(p)
			else:
				for g in profilegroup:
					if g['id'] in usergroups:
						profiles.append(p)
		query=Profile.objects.filter(Q(groups=None)|Q(groups=usergroups[0]))
		for group in usergroups[1:]:
			query=query.filter(groups=group)
        	self.fields['profile'].queryset = query
	class Meta:
		model = VM
		fields = ['name', 'physical', 'ip1','mac1', 'ipilo', 'ip2', 'mac2', 'ip3', 'mac3', 'ip4', 'mac4', 'iso', 'virtualprovider', 'cobblerprovider', 'foremanprovider', 'hostgroup' , 'profile', 'type', 'puppetclasses','puppetparameters', 'cobblerparameters']
		


class StorageForm(ModelForm):
	class Meta:
		model = Storage

class ApacheForm(ModelForm):
	class Meta:
		model = Apache

class OracleForm(ModelForm):
	class Meta:
		model = Oracle

class RacForm(ModelForm):
	class Meta:
		model = Rac

class SapForm(ModelForm):
	class Meta:
		model = Sap

class WeblogicForm(ModelForm):
	class Meta:
		model = Weblogic

class PartitioningForm(ModelForm):
	class Meta:
		model = Partitioning
