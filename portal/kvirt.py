#-*- coding: utf-8 -*-

import os
import sys
import time
import libvirt
import xml.etree.ElementTree as ET

KB = 1024*1024
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

class Kvirt:
 def __init__(self,host,port,user,protocol='ssh'):
    if user and port :
        url = "qemu+%s://%s@%s:%s/system" % (protocol,user,host,port)
    elif port:
        url = "qemu+%s://%s:%s/system" % (protocol,host,port)
    else:
        url = "qemu///system"
	self.macaddr = []
    self.conn = libvirt.open(url)
    self.host = host
    self.macaddr = []


 def close(self):
	conn=self.conn
	conn.close()
	self.conn=None


 def create(self, name, clu, numcpu, numinterfaces, netinterface, diskformat1, disksize1, diskinterface,memory, storagedomain, guestid, net1, net2=None, net3=None, net4=None, mac1=None, mac2=None,launched=True, iso=None, diskformat2=None, disksize2=None):
	conn=self.conn
	type,machine,emulator = 'kvm','pc','/usr/libexec/qemu-kvm'
	memory = memory*1024
	disksize1 = disksize1*GB
        #disksize1 = int(disksize1) * 1073741824
        if disksize2:
                disksize2 = disksize2*GB
	storagename = "%s.img" % name
        storagepool = conn.storagePoolLookupByName(storagedomain)
        poolxml = storagepool.XMLDesc(0)
        root = ET.fromstring(poolxml)
        for element in root.getiterator('path'):
            storagepath = element.text
	    break
	allocation = 0
        diskxml = """<volume>
  			<name>%s</name>
  			<key>%s/%s</key>
  			<source>
  			</source>
  			<capacity unit='bytes'>%s</capacity>
  			<allocation unit='bytes'>0</allocation>
  			<target>
    			<path>%s/%s</path>
    			<format type='%s'/>
  			</target>
			</volume>""" % (storagename, storagepath,storagename,disksize1,  storagepath,storagename,diskformat1)
        storagepool.createXML(diskxml, 0)
	storagepool.refresh(0)
	diskdev,diskbus = 'vda','virtio'
	if diskinterface != 'virtio':
		diskdev,diskbus = 'hda','ide'

	#create xml
        vmxml = """<domain type='%s'>
                  <name>%s</name>
                  <memory>%d</memory>
                  <vcpu>%s</vcpu>
                  <os>
                    <type arch='x86_64' machine='%s'>hvm</type>
                    <boot dev='hd'/>
                    <boot dev='cdrom'/>
                    <bootmenu enable='yes'/>
                  </os>
                  <features>
                    <acpi/>
                    <apic/>
                    <pae/>
                  </features>
                  <clock offset='utc'/>
                  <on_poweroff>destroy</on_poweroff>
                  <on_reboot>restart</on_reboot>
                  <on_crash>restart</on_crash>
                  <devices>
                    <emulator>%s</emulator>
                    <disk type='file' device='disk'>
                      <driver name='qemu' type='%s'/>
                      <source file='%s/%s'/>
	      <target dev='%s' bus='%s'/>
    		</disk>
                <disk type='file' device='cdrom'>
                      <driver name='qemu' type='raw'/>
                      <source file=''/>
                      <target dev='hdc' bus='ide'/>
                      <readonly/>
                  </disk>
		<interface type='network'>
                  <source network='%s'/>
		<model type='virtio'/>
		</interface>
                 <input type='tablet' bus='usb'/>
                 <input type='mouse' bus='ps2'/>
                <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0'>
                 <listen type='address' address='0.0.0.0'/>
                </graphics>
                <memballoon model='virtio'/>
                </devices>
                </domain>""" % (type, name, memory, numcpu, machine,emulator, diskformat1, storagepath,storagename, diskdev, diskbus, net1)
	conn.defineXML(vmxml)
        vm = conn.lookupByName(name)
        vm.setAutostart(1)
        xml = vm.XMLDesc(0)
        root = ET.fromstring(xml)
	macs={}
        for element in root.getiterator('interface'):
		mac = element.find('mac').get('address')
		network = element.find('source').get('network')
		bridge = element.find('source').get('bridge')
		if bridge:
			macs[bridge]=mac
		else:
			macs[network]=mac
	for net in [net1,net2,net3,net4]:
		if not net:
			break
		else:
			self.macaddr.append(macs[net])

 def start(self,name):
    conn = self.conn
    status = {0:'down',1:'up'}
    vm = conn.lookupByName(name)
    vm.create()
    return "%s started" % name

 def stop(self,name):
    conn = self.conn
    status = {0:'down',1:'up'}
    vm = conn.lookupByName(name)
    if status[vm.isActive()]=="down":
   		return "VM allready stopped"
    else:
  		vm.destroy()
    return "%s stopped" % name

 def getstorage(self):
    results={}
    conn = self.conn
    for storage in conn.listStoragePools():
        storagename = storage
        storage = conn.storagePoolLookupByName(storage) 
        s= storage.info()
        used = "%.2f" % ( float(s[2])/1024/1024/1024 )
        available = "%.2f" % ( float(s[3])/1024/1024/1024 )
        #Type,Status, Total space in Gb, Available space in Gb
        results[storagename ] = [float(used), float(available),storagename]
    return results

 def beststorage(self):
    bestsize = 0
    beststoragedomain = ''
    conn = self.conn
    for storage in conn.listStoragePools():
        storagename = storage
        storage = conn.storagePoolLookupByName(storage) 
        s= storage.info()
        used = float(s[2])/1024/1024/1024
        available = float(s[3])/1024/1024/1024
        if available > bestsize:
            beststoragedomain = storagename
            bestsize = available
	return beststoragedomain

 def status(self,name):
    conn = self.conn
    status = {0:'down',1:'up'}
    vm = conn.lookupByName(name)
    if not vm:
  		return None
    else:
		return status[vm.isActive()]

 def allvms(self):
    conn = self.conn
    status = {0:'down',1:'up'}
    vms = {}
    for vm in conn.listAllDomains(0):
        vms[vm.name()] = status[vm.isActive()]
    return vms

 def console(self,name):
    conn = self.conn
    vm = conn.lookupByName(name)
    if not vm:
  		return None
    else:
        xml = vm.XMLDesc(0)
        root = ET.fromstring(xml)
        for element in root.getiterator('graphics'):
            attributes = element.attrib
	    if attributes['listen'] == '127.0.0.1':
                return None,None,None,None
            protocol = attributes['type']
            port = attributes['port']
            if protocol=="spice":
                #sport = attributes['tlsPort']
                return self.host,port,None,protocol
            else:
                return self.host,port,None,protocol

 def getisos(self):
    isos=[]
    conn = self.conn
    for storage in conn.listStoragePools():
        storage = conn.storagePoolLookupByName(storage) 
        for volume in storage.listVolumes():
            if volume.endswith('iso'):
                isos.append(volume)
    return isos

 def remove(self,name):
	conn = self.conn
	vm = conn.lookupByName(name)
	status = {0:'down',1:'up'}
	vm = conn.lookupByName(name)
#	print dir(vm)
#	xml = vm.XMLDesc(0)
#	root = ET.fromstring(xml)
#	for element in root.getiterator('graphics'):
#            attributes = element.attrib
#	return
	if status[vm.isActive()]!="down":
		vm.destroy()
	vm.undefine()
	print "VM %s killed" % name
	return True
