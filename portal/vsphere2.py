
import os 
import sys
from pysphere import VIServer,VIProperty,VIMor,MORTypes

class Vsphere:
 def __init__(self, vcip, vcuser, vcpassword, dc, clu):
	self.vcip = vcip
	self.translation = {'POWERED OFF':'down', 'POWERED ON':'up'}
	s = VIServer()
	s.connect(vcip, vcuser, vcpassword)
	self.s = s
	self.clu = clu
	self.dc = dc
#	self.clu = s._get_clusters()[clu]
#	clusters = s.get_clusters()
#	for mor in clusters:
#		if clusters[mor]==clu:
#			self.clu = mor
#			break
	#self.dc = dc
#	self.dc = s._get_datacenters()[dc]
#	hosts ={}
#	for host in s.get_hosts(from_mor=self.clu):
#		hosts[s.get_hosts(from_mor=self.clu)[host]]=host


 def create(self, name, numcpu, numinterfaces, diskmode1,disksize1, ds, memory, guestid, net1, net2=None, net3=None, net4=None, thin=False,distributed=False,diskmode2=None,disksize2=None,vnc=False):
	s = self.s


 def start(self, name):
	s = self.s
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	if vm.get_status() == 'POWERED OFF':
		vm.power_on()

 def remove(self, name):
	s = self.s
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
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	return translation[vm.get_status()]

 def console(self, name):
	s = self.s
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
        vncfound = False
	for config in vm.properties.config.extraConfig:
                key, value = config.key, config.value
                if 'vnc' in key:
                        vncfound = True
                        vncport = value
                        break
                else:
                        continue
        if vncfound:
		host = vm.properties.runtime.host.name
                return host,vncport
        else:
                return None,None

 def html5console(self, name, fqdn, sha1):
	vcip = self.vcip
	vcconsoleport = "7331"
	s = self.s
	dc = self.dc
	try:
		vm =  s.get_vm_by_name(name)
	except:
		print "vm %s not found" % name
		return
	session = s.acquire_clone_ticket()
	vmid = vm._mor
	vmurl = "http://%s:%s/console/?vmId=%s&vmName=%s&host=%s&sessionTicket=%s&thumbprint=%s" % (vcip, vcconsoleport, vmid, name, fqdn, session, sha1)
	return vmurl
	
 def allvms(self):
	vms={}
	s = self.s
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
	dc = s._get_datacenters()[self.dc]
	dcprop = VIProperty(s, dc)
	dc = dcprop.name
	dcs = s.get_datacenters()
#	for mor, name in dcs.items():
#        	if name == self.dc:
#			dcmor = mor
#			break
#	clusters = s.get_clusters(from_mor=dcmor)
#	for mor, name in clusters.items():
#        	if name == self.clu:
#			clumor = mor
#			break
#	hosts = s.get_hosts(from_mor=clumor)
#	for mor, name in hosts.items():
#		print mor,name
#		hostprop = VIProperty(s, mor)
#		print hostprop.vm
	results = {}
        for dts in s.get_datastores():
		props=VIProperty(s, dts)
		vms = props.vm	
		clumember = False
#		for vm  in vms: 
#			print vm._obj
#			#vm = VIProperty(s, mor)
#			#vm =  s.get_vm_by_name(vm.name)
#			#print vm.properties.runtime.host.name
#			break
		datastorename = props.name
		total = props.summary.capacity / 1024 / 1024 /1024
		available = props.summary.freeSpace / 1024 / 1024 /1024
		results[datastorename] = [total, available, dc]
        return results

 def beststorage(self):
	s = self.s
	dc = self.dc
	clu = self.clu
