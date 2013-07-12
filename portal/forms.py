#-*- coding: utf-8 -*-
from django.forms import ModelForm
from portal.models import VM,Storage,Oracle,Apache,Rac,Sap,Weblogic,Partitioning

class VMForm(ModelForm):
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
