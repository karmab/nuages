#-*- coding: utf-8 -*-

import os
import sys
import time
import libvirt
import xml.etree.ElementTree as ET

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

 def close(self):
	conn=self.conn
	conn.close()
	self.conn=None

 def create(self, name, clu, numcpu, numinterfaces, netinterface, diskformat1, disksize1, diskinterface,memory, storagedomain, guestid, net1, net2=None, net3=None, net4=None, mac1=None, mac2=None,launched=True, iso=None, diskformat2=None, disksize2=None):
    return "prout"

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
    for ID in conn.listDomainsID():
        vm = conn.lookupByID(ID)
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
            protocol = attributes['type']
            port = attributes['port']
            if protocol=="spice":
                sport = attributes['sport']
                return self.host,sport,None,protocol
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
    vm.undefine()
    print "VM %s killed" % name
    return True
