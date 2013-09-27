
import os 
import sys
from pysphere import VIServer,VIProperty

class Vsphere:
 def __init__(self, vcip, vcuser, vcpassword, dc, clu):
	self.translation = {'POWERED OFF':'down', 'POWERED ON':'up'}
	s = VIServer()
	s.connect(vcip, vcuser, vcpassword)
	self.s = s
	self.clu = s._get_clusters()[clu]
#	clusters = s.get_clusters()
#	for mor in clusters:
#		if clusters[mor]==clu:
#			self.clu = mor
#			break
	#self.dc = dc
	self.dc = s._get_datacenters()[dc]
	hosts ={}
	for host in s.get_hosts(from_mor=self.clu):
		hosts[s.get_hosts(from_mor=self.clu)[host]]=host


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
	if vm.get_status() == 'POWERED ON':
		vm.power_off()
	vm.destroy()

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
	translation = self.translation
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
	vms={}
	s = self.s
	dc = self.dc
	clu = self.clu
	translation = self.translation
	up = s.get_registered_vms(status='poweredOn')
	down = s.get_registered_vms(status='poweredOff')
	for path in up:
		name = path.split('/')[1].replace('.vmx','')
		vms[name] = 'up'
	for path in down:
		name = path.split('/')[1].replace('.vmx','')
		vms[name] = 'down'
	return sorted(vms)
		

 def getstorage(self):
	s = self.s
        dc = self.dc
        clu = self.clu
        results = {}
        for dts in s.get_datastores():
		props=VIProperty(s, dts)
		vms = props.vm
		for vm  in vms: 
			mor = vm._obj
			vm = VIProperty(s, mor)
			vm =  s.get_vm_by_name(vm.name)
			print vm.get_properties()
			break
		datastorename = props.name
		total = props.summary.capacity / 1024 / 1024 /1024
		available = props.summary.freeSpace / 1024 / 1024 /1024
		#print props._values
		results[datastorename] = [total, available, dc]
        return results


 def beststorage(self):
	s = self.s
	dc = self.dc
	clu = self.clu
