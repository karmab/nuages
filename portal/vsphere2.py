#!/usr/bin/env jython

import os 
import sys
from pysphere import VIServer



class Vsphere:
 def __init__(self, vcip, vcuser, vcpassword, dc, clu):
	s = VIServer()
	s.connect(vcip, vcuser, vcpassword)
	self.s = s
	self.dc = dc
	self.clu = clu


 def create(self, name, numcpu, numinterfaces, diskmode1,disksize1, ds, memory, guestid, net1, net2=None, net3=None, net4=None, thin=False,distributed=False,diskmode2=None,disksize2=None,vnc=False):
	s = self.s
	dc = self.dc
	clu = self.clu


 def start(self, name):
	s = self.s
	dc = self.dc
	clu = self.clu
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	if vm.get_status() == 'POWERED OFF':
		vm.power_on()

 def remove(self, name):
	s = self.s
	dc = self.dc
	clu = self.clu
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return

 def stop(self, name):
	s = self.s
	dc = self.dc
	clu = self.clu
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	if vm.get_status() == 'POWERED ON':
		vm.power_off()

 def status(self, name):
	translation = {'POWERED OFF':'down', 'POWERED ON':'up'}
	s = self.s
	dc = self.dc
	clu = self.clu
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	return translation[vm.get_status()]

 def console(self, name):
	s = self.s
	dc = self.dc
	clu = self.clu
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	print "console"

 def html5console(self, name, fqdn, sha1):
	s = self.s
	dc = self.dc
	clu = self.clu
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return

 def allvms(self):
	s = self.s
	dc = self.dc
	clu = self.clu
	translation = {'POWERED OFF':'down', 'POWERED ON':'up'}
	allvms = s.get_registered_vms()
	print allvms

 def getstorage(self):
	s = self.s
	dc = self.dc
	clu = self.clu


 def beststorage(self):
	s = self.s
	dc = self.dc
	clu = self.clu
