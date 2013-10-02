#-*- coding: utf-8 -*-

import datetime
import os
import sys
import time
from ovirtsdk.api import API
from ovirtsdk.xml import params
import StringIO

MB = 1024*1024
GB = 1024*MB
guestrhel332 = "rhel_3"
guestrhel364 = "rhel_3x64"
guestrhel432 = "rhel_4"
guestrhel464 = "rhel_4x64"
guestrhel532 = "rhel_5"
guestrhel564 = "rhel_5x64"
guestrhel632 = "rhel_6"
guestrhel664 = "rhel_6x64"
guestother = "other"
guestotherlinux = "other_linux"
guestwindowsxp = "windows_xp"
guestwindows7 = "windows_7"
guestwindows764 = "windows_7x64"
guestwindows2003 = "windows_2003"
guestwindows200364 = "windows_2003x64"
guestwindows2008 = "windows_2008"
guestwindows200864 = "windows_2008x64"

def checkiso(api, iso=None):
 isodomains = []
 datacenters = api.datacenters.list()
 for ds in datacenters:
  for sd in ds.storagedomains.list():
   if sd.get_type()=="iso" and sd.get_status().get_state()=="active":
       isodomains.append(sd)
 if len(isodomains)==0:
  print "No iso domain found.Leaving..."
  sys.exit(1)
 for sd in isodomains:
  isodomainid = sd.get_id()
  sdfiles = api.storagedomains.get(id=isodomainid).files
  for f in sdfiles.list():
   if not iso:
    print f.get_id()
   elif f.get_id()==iso:
     return f

######OVIRT PARAMETERS
#ohost
#oport
#ouser
#opassword
#ossl
#clu
#numcpu
#diskformat
#diskinterface
#disksize (*GB)
#memory ( *MB)
#storagedomain
#numinterfaces
#netinterface

class Ovirt:
 def __init__(self,ohost,oport,ouser,opassword,ossl):
	if ossl:
 		url = "https://%s:%s/api" % (ohost, oport)
	else:
 		url = "http://%s:%s/api" % (ohost, oport)
	self.api = API(url=url, username=ouser, password=opassword, insecure=True)
	self.macaddr = []

 def close(self):
	api=self.api
	api.disconnect()
	self.api=None

 def create(self, name, clu, numcpu, numinterfaces, netinterface, diskformat1, disksize1, diskinterface,memory, storagedomain, guestid, net1, net2=None, net3=None, net4=None, mac1=None, mac2=None,launched=True, iso=None, diskformat2=None, disksize2=None,vnc=False):
	boot1,boot2='hd','network'
	if iso in ["","xx","yy"]:
		iso=None
	if iso:
		boot2='cdrom'
	api=self.api
	memory = memory*MB
	disksize1 = disksize1*GB
	if disksize2:
		disksize2 = disksize2*GB
	#VM CREATION IN OVIRT
	#TODO check that clu and storagedomain exist and that there is space there
	sparse = True
	if diskformat1=="raw":
		sparse1=False
	if diskformat2 and diskformat2=="raw":
		sparse2=False
	vm = api.vms.get(name=name)
	if vm:
 		return "VM %s allready existing.Leaving...\n" % name
	clu = api.clusters.get(name=clu)
	storagedomain = api.storagedomains.get(name=storagedomain)
	try:
 		disk1 = params.Disk(storage_domains=params.StorageDomains(storage_domain=[storagedomain]), name="%s_Disk1" % (name), size=disksize1, type_='system', status=None, interface=diskinterface, format=diskformat1, sparse=sparse1, bootable=True)
 		disk1 = api.disks.add(disk1)
 		disk1id = disk1.get_id()
	except:
 		return "Insufficient space in storage domain for disk1.Leaving...\n"
	if disksize2:
		try:
 			disk2 = params.Disk(storage_domains=params.StorageDomains(storage_domain=[storagedomain]), name="%s_Disk2" % (name), size=disksize2, type_='system', status=None, interface=diskinterface, format=diskformat2, sparse=sparse2, bootable=False)
 			disk2 = api.disks.add(disk2)
 			disk2id = disk2.get_id()
		except:
 			return "Insufficient space in storage domain for disk2.Leaving...\n"
	
	#boot order
	boot = [params.Boot(dev=boot1),params.Boot(dev=boot2)]
	#vm creation
	kernel,initrd,cmdline=None,None,None
	if vnc:
		display=params.Display(type_='vnc')
	else:
		display=params.Display(type_='spice')
	api.vms.add(params.VM(name=name, memory=memory, cluster=clu, display=display, template=api.templates.get('Blank'), os=params.OperatingSystem(type_=guestid, boot=boot, kernel=kernel, initrd=initrd, cmdline=cmdline), cpu=params.CPU(topology=params.CpuTopology(cores=numcpu)), type_="server"))
	#add nics
	api.vms.get(name).nics.add(params.NIC(name='eth0', network=params.Network(name=net1), interface=netinterface))

	if numinterfaces>=2:
    		api.vms.get(name).nics.add(params.NIC(name='eth1', network=params.Network(name=net2), interface=netinterface))
    		#compare eth0 and eth1 to get sure eth0 has a lower mac
    		eth0ok = True
    		maceth0 = api.vms.get(name).nics.get(name="eth0").mac.address
    		maceth1 = api.vms.get(name).nics.get(name="eth1").mac.address
    		eth0 = maceth0.split(":")
    		eth1 = maceth1.split(":")
    		for i in range(len(eth0)):
        		el0 = int(eth0[i], 16)
        		el1 = int(eth1[i], 16)
        		if el0 == el1: 
            			pass
        		elif el0 > el1:
            			eth0ok=False

    		if not eth0ok:
        		tempnic = "11:11:11:11:11:11"   
        		nic = api.vms.get(name).nics.get(name="eth0")
        		nic.mac.address = tempnic
        		nic.update()
        		nic = api.vms.get(name).nics.get(name="eth1")
        		nic.mac.address = maceth0
        		nic.update()
        		nic = api.vms.get(name).nics.get(name="eth0")
        		nic.mac.address = maceth1
        		nic.update()
     
	if mac1:
 		nic = api.vms.get(name).nics.get(name="eth0")
 		if not ":" in mac1:
     			mac1 = "%s%s" % (nic.mac.address[:-2], mac1)
 		nic.mac.address = mac1
 		nic.update()

	if mac2:
 		nic = api.vms.get(name).nics.get(name="eth1")
 		if not ":" in mac2:
     			mac2 = "%s%s" % (nic.mac.address[:-2], mac2)
 		nic.mac.address = mac2
 		nic.update()

	if numinterfaces>=3:
    		api.vms.get(name).nics.add(params.NIC(name='eth2', network=params.Network(name=net3), interface=netinterface))
	if numinterfaces>=4:
    		api.vms.get(name).nics.add(params.NIC(name='eth3', network=params.Network(name=net4), interface=netinterface))
	api.vms.get(name).update()
	if iso:
 		iso = checkiso(api,iso)
 		cdrom = params.CdRom(file=iso)
 		api.vms.get(name).cdroms.add(cdrom)
	while api.disks.get(id=disk1id).get_status().get_state() != "ok":
 		time.sleep(5)
	api.vms.get(name).disks.add(disk1)
	while not api.vms.get(name).disks.get(id=disk1id):
 		time.sleep(2)
	api.vms.get(name).disks.get(id=disk1id).activate()
	if disksize2:
		while api.disks.get(id=disk2id).get_status().get_state() != "ok":
 			time.sleep(5)
		api.vms.get(name).disks.add(disk2)
		while not api.vms.get(name).disks.get(id=disk2id):
 			time.sleep(2)
		api.vms.get(name).disks.get(id=disk2id).activate()
	#retrieve MACS for cobbler
	vm = api.vms.get(name=name)
	for nic in vm.nics.list():
		self.macaddr.append(nic.mac.address)


 def getmacs(self,name):
	api=self.api
	vm = api.vms.get(name=name)
	if not vm:
		return None
	macs=[]
	for nic in vm.nics.list():
		address = nic.mac.address
		net = api.networks.get(id=nic.network.id).get_name()
		macs.append("%s=%s" % (net,address))
	return macs

 def start(self,name):
	api=self.api
 	while api.vms.get(name).status.state =="image_locked":
  		time.sleep(5) 
	launched = False
	api.vms.get(name).start()
	return "%s started" % name
	#while not launched:
	#	try:
	#		api.vms.get(name).start()
	#		launched = True
	#		return "%s started" % name
	#	except:
	#		time.sleep(5)
	#		continue
 def stop(self,name):
	api=self.api
  	if api.vms.get(name).status.state=="down":
   		return "VM allready stopped"
	else:
  		api.vms.get(name).stop()
	return "%s stopped" % name


 def getstorage(self):
	results={}
	api=self.api
	datacenters = api.datacenters.list()
 	for ds in datacenters:
  		#print "Datacenter: %s Type: %s Status: %s" % (ds.name, ds.storage_type, ds.get_status().get_state())
  		for s in ds.storagedomains.list():
			if s.get_status().get_state()=="active" and s.get_type()=="data":
    					used = s.get_used()/1024/1024/1024
    					available = s.get_available()/1024/1024/1024
    					#Type,Status, Total space in Gb, Available space in Gb
    					results[s.name ] = [used, available,ds.name]
	return results

# def beststorage(self):
#	results={}
#	api=self.api
#	datacenters = api.datacenters.list()
#	bestsize = 0
#	beststoragedomain = ''
# 	for ds in datacenters:
#  		for s in ds.storagedomains.list():
#			if s.get_status().get_state()=="active" and s.get_type()=="data":
#    					used = s.get_used()/1024/1024/1024
#    					available = float(s.get_available()/1024/1024/1024)
#					if available > bestsize:
#						beststoragedomain = s.name
#						bestsize = available
#	return beststoragedomain

 def beststorage(self,datacenter):
	results={}
	api=self.api
	datacenter = api.datacenters.get(name=datacenter)
	bestsize = 0
	beststoragedomain = ''
  	for s in datacenter.storagedomains.list():
		if s.get_status().get_state()=="active" and s.get_type()=="data":
			used = s.get_used()/1024/1024/1024
			available = float(s.get_available()/1024/1024/1024)
			if available > bestsize:
				beststoragedomain = s.name
				bestsize = available
	return beststoragedomain


 def status(self,name):
	api=self.api
	vm =api.vms.get(name=name)
 	if not vm:
  		return None
	else:
		return vm.status.state

 def allvms(self):
	api=self.api
	vms={}
	for vm in api.vms.list():
		vms[vm.name] = vm.status.state
	return vms


 def console(self,name):
	api=self.api
	vm =api.vms.get(name=name)
 	if not vm or vm.status.state=="down":
  		return None,None,None,None
	else:
  		vm.ticket().set_ticket("")
  		ticket = vm.ticket().get_ticket().get_value()
  		host,port,sport=vm.get_display().get_address(),vm.get_display().get_port(),vm.get_display().get_secure_port()
		protocol=vm.get_display().get_type()
  		if protocol=="spice":
			return host,sport,ticket,protocol
		elif protocol=="vnc":
			return host,port,ticket,protocol


 def getisos(self):
	api=self.api
	isos=[]
 	isodomains = []
 	datacenters = api.datacenters.list()
 	for ds in datacenters:
  		for sd in ds.storagedomains.list():
   			if sd.get_type()=="iso" and sd.get_status().get_state()=="active":
       				isodomains.append(sd)
 	if len(isodomains)==0:
 		 #return "No iso domain found.Leaving..."
 		 return isos
 	for sd in isodomains:
  		isodomainid = sd.get_id()
  		sdfiles = api.storagedomains.get(id=isodomainid).files
  		for f in sdfiles.list():
    			isos.append(f.get_id())
	return isos

 def checknetwork(self,cluster,netname):
	api = self.api
	clu = api.clusters.get(name=cluster)
	for net in clu.networks.list():
		if net.name == netname:
			return True
	return False

 def checkcluster(self,cluster):
	api = self.api
	clu = api.clusters.get(name=cluster)
	if not clu:
		return False	
	return True

 def remove(self,name):
	api = self.api
	if api.vms.get(name).status.state=="up" or api.vms.get(name).status.state=="powering_up" or api.vms.get(name).status.state=="reboot_in_progress":
   		api.vms.get(name).stop()
   		print "VM %s stopped" % name
 	while api.vms.get(name).status.state !="down":
  		time.sleep(4) 
  	api.vms.get(name).delete()
	print "VM %s killed" % name
	return True
