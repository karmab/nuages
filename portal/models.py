# -*- coding: iso-8859-15 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User,Group
import ast
import os
import subprocess
import time
from django.conf import settings
hooks = settings.PWD+'/hooks'


try:
    from portal.ovirt import Ovirt
except:
    print "Missing ovirt-engine-sdk package for ovirt support"
try:
    from portal.kvirt import Kvirt
except:
    print "Missing libvirt-python package for libvirt support"

from portal.cobbler import Cobbler
try:
    from portal.foreman import Foreman
except:
    print "Missing python-requests package for foreman support"
import django.utils.simplejson as json
import time,datetime
from random import choice
import json
from django.contrib.auth.decorators import login_required
import logging
import random
try:
    from portal.ilo import Ilo
except:
    print "Missing python-paramiko package for ilo support"
try:
    from portal.oa import Oa
except:
    print "Missing python-paramiko package for oa support"
import socket
from django.forms import ModelForm
from django.db.models import Q
from datetime import datetime


#default values
DISKSIZE = '10'
MEMORY = 512
CPUS = 1
NUMINTERFACES = 1
NET1 = 'ovirtmgmt'
SUBNET1 = '255.255.255.0'
DISKINTERFACE = 'virtio'
NETINTERFACE = 'virtio'
PHYSICALPORT = 22
VIRTUALPORT = 443
COBBLERPORT = 80
FOREMANPORT = 80
FOREMANARCH = 'x86_64'
FOREMANENV = 'production'
FOREMANOS = 'rhel'
FOREMANPUPPET = 'puppet'
LDAPSSLPORT = 636

def checkconn(host,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        return True
    except socket.error:
        return False

def nonone(variable):
    if variable == None:
        return ''
    else:
        return str(variable)
        #try:
        #    name= variable.name
        #    return name
        #except:
        #    return str(variable)

class IpamProvider(models.Model):
    name                = models.CharField(max_length=80)
    host                = models.CharField(max_length=60)
    port                = models.IntegerField(default=80)
    user                = models.CharField(max_length=60)
    password            = models.CharField(max_length=20)
    type                = models.CharField(max_length=10, default='naman')
    def __unicode__(self):
        return self.name

class LdapProvider(models.Model):
    name                = models.CharField(max_length=80)
    host                = models.CharField(max_length=60,blank=True, null=True)
    basedn              = models.CharField(max_length=160,blank=True, null=True)
    binddn              = models.CharField(max_length=160,blank=True, null=True)
    bindpassword        = models.CharField(max_length=20,blank=True, null=True)
    secure              = models.BooleanField(default=True)
    userfield           = models.CharField(max_length=60)
    certname            = models.CharField(max_length=60,blank=True, null=True)
    filter1             = models.CharField(max_length=160,blank=True, null=True)
    filter2             = models.CharField(max_length=160,blank=True, null=True)
    filter3             = models.CharField(max_length=160,blank=True, null=True)
    filter4             = models.CharField(max_length=160,blank=True, null=True)
    groups1             = models.ManyToManyField(Group,blank=True,null=True,related_name='groups1')
    groups2             = models.ManyToManyField(Group,blank=True,null=True,related_name='groups2')
    groups3             = models.ManyToManyField(Group,blank=True,null=True,related_name='groups3')
    groups4             = models.ManyToManyField(Group,blank=True,null=True,related_name='groups4')
    def __unicode__(self):
        return self.name
    def clean(self):
        if self.secure:
            if not self.certname:
                raise ValidationError("Secure mode requires to set a cert name")
            elif not os.path.exists("%s/%s" % (settings.PWD, self.certname) ):
                raise ValidationError("Secure mode requires to put %s in %s" % (self.certname, settings.PWD) )


class PhysicalProvider(models.Model):
    name                = models.CharField(max_length=80)
    user                = models.CharField(max_length=60)
    password            = models.CharField(max_length=20)
    type                = models.CharField(max_length=20, default='ilo',choices=( ('ilo', 'ilo'),('oa','oa'),('drac', 'drac'),('ssh', 'ssh'),('fake', 'fake') ))
    def __unicode__(self):
        return self.name

class VirtualProvider(models.Model):
    name                = models.CharField(max_length=80)
    host                = models.CharField(max_length=60,blank=True, null=True)
    port                = models.IntegerField(default=VIRTUALPORT)
    user                = models.CharField(max_length=60)
    password            = models.CharField(max_length=20)
    type                = models.CharField(max_length=20, default='ovirt',choices=( ('ovirt', 'ovirt'),('vsphere', 'vsphere'),('kvirt', 'libvirt'),('fake', 'fake') ))
    ssl                 = models.BooleanField(default=True)
    clu                 = models.CharField(max_length=50,blank=True)
    datacenter          = models.CharField(max_length=50, blank=True)
    active              = models.BooleanField(default=True)
    sha1                = models.CharField(max_length=80,blank=True, null=True)
    fqdn                = models.CharField(max_length=60,blank=True, null=True)
    def __unicode__(self):
        return self.name
    def clean(self):
        if not self.host:
            raise ValidationError("Host cant be blank")

class ForemanProvider(models.Model):
    name                = models.CharField(max_length=80)
    host                = models.CharField(max_length=60,blank=True, null=True)
    port                = models.IntegerField(default=FOREMANPORT)
    secure              = models.BooleanField(default=False)
    user                = models.CharField(max_length=60, blank=True, null=True)
    password            = models.CharField(max_length=20, blank=True, null=True)
    mac                 = models.CharField(max_length=20, blank=True, null=True)
    osid                = models.CharField(max_length=20, default=FOREMANOS,  blank=True, null=True)
    envid               = models.CharField(max_length=20, default=FOREMANENV, blank=True, null=True)
    archid              = models.CharField(max_length=20, default=FOREMANARCH, blank=True, null=True)
    puppetid            = models.CharField(max_length=20, default=FOREMANPUPPET, blank=True, null=True)
    ptableid             = models.CharField(max_length=20, blank=True, null=True)
    def __unicode__(self):
        return self.name
    def clean(self):
        if not self.host:
            raise ValidationError("Host cant be blank")

class CobblerProvider(models.Model):
    name                = models.CharField(max_length=80)
    host                = models.CharField(max_length=60,blank=True, null=True)
    user                = models.CharField(max_length=60, blank=True)
    password            = models.CharField(max_length=20, blank=True)
    def __unicode__(self):
        return self.name
    def clean(self):
        if not self.host:
            raise ValidationError("Host cant be blank")

class Storage(models.Model):
    name              = models.CharField(max_length=80)
    type              = models.CharField(max_length=20, default='ovirt',choices=( ('ovirt', 'ovirt'),('vsphere', 'vsphere' )))
    provider          = models.ForeignKey(VirtualProvider)
    datacenter        = models.CharField(max_length=50,blank=True)
    def __unicode__(self):
        return "%s %s" % (self.provider,self.name)

class Hook(models.Model):
    name              = models.CharField(max_length=80)
    type              = models.CharField(max_length=20, default='python',choices=( ('python', 'python'),('bash', 'bash'),('perl', 'perl'),('ruby', 'ruby') ))
    content           = models.TextField()
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        f = open("%s/%s" % (hooks, self.name),'w')
        f.write(self.content.replace('\r',''))
        f.close()
        super(Hook, self).save(*args, **kwargs)

class Profile(models.Model):
    name              = models.CharField(max_length=80)
    physicalprovider  = models.ForeignKey(PhysicalProvider,blank=True,null=True)
    virtualprovider   = models.ForeignKey(VirtualProvider,blank=True,null=True)
    cobblerprovider   = models.ForeignKey(CobblerProvider,blank=True,null=True)
    foremanprovider   = models.ForeignKey(ForemanProvider,blank=True,null=True)
    ipamprovider      = models.ForeignKey(IpamProvider,blank=True,null=True)
    cobblerprofile    = models.CharField(max_length=40,blank=True)
    datacenter        = models.CharField(max_length=50)
    template          = models.CharField(max_length=80,blank=True,null=True)
    clu               = models.CharField(max_length=50,blank=True)
    guestid           = models.CharField(max_length=20, choices=( ('rhel_6x64', 'rhel_6x64'),('rhel_5x64', 'rhel_5x64'),('windows_xp', 'windows_xp') ))
    memory            = models.IntegerField(default=MEMORY)
    numcpu            = models.IntegerField(default=CPUS)
    disksize1         = models.IntegerField(default=10)
    diskthin1         = models.BooleanField(default=True)
    disksize2         = models.IntegerField(blank=True,null=True)
    diskthin2         = models.BooleanField(default=True)
    nextserver        = models.CharField(max_length=80, blank=True)
    numinterfaces     = models.IntegerField(default=NUMINTERFACES)
    net1              = models.CharField(max_length=40, default=NET1)
    subnet1           = models.GenericIPAddressField(default=SUBNET1, blank=True, null=True, protocol="IPv4")
    net2              = models.CharField(max_length=40, blank=True)
    subnet2           = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    net3              = models.CharField(max_length=40, blank=True)
    subnet3           = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    net4              = models.CharField(max_length=40, blank=True)
    subnet4           = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    diskinterface     = models.CharField(max_length=20, default=DISKINTERFACE)
    netinterface      = models.CharField(max_length=20, default=NETINTERFACE)
    cmdline           = models.CharField(max_length=200,blank=True)
    rootpw            = models.CharField(max_length=60,blank=True,null=True)
    dns               = models.CharField(max_length=60,blank=True,null=True)
    dns1              = models.CharField(max_length=60,blank=True,null=True)
    cloudinit         = models.BooleanField(default=False)
    autostorage       = models.BooleanField(default=True)
    foreman           = models.BooleanField(default=False)
    foremanparameters = models.BooleanField(default=False)
    cobbler           = models.BooleanField(default=False)
    cobblerparameters = models.BooleanField(default=False)
    iso               = models.BooleanField(default=False)
    hide              = models.BooleanField(default=True)
    console           = models.BooleanField(default=False)
    requireip         = models.BooleanField(default=False)
    deletable         = models.BooleanField(default=True)
    vnc               = models.BooleanField(default=False)
    price             = models.IntegerField(blank=True,null=True)
    maxvms            = models.IntegerField(blank=True,null=True)
    hookbeforecreate  = models.ForeignKey(Hook,blank=True,null=True,related_name='hookbeforecreate')
    hookaftercreate   = models.ForeignKey(Hook,blank=True,null=True,related_name='hookaftercreate')
    hookbeforestart   = models.ForeignKey(Hook,blank=True,null=True,related_name='hookbeforestart')
    hookafterstart    = models.ForeignKey(Hook,blank=True,null=True,related_name='hookafterstart')
    hookafterbuild    = models.ForeignKey(Hook,blank=True,null=True,related_name='hookafterbuild')
    groups            = models.ManyToManyField(Group,blank=True,null=True)
    def __unicode__(self):
        return self.name
    def clean(self):
        if self.numinterfaces >=1 and not self.net1:
            raise ValidationError("Net1 is required")
        if self.numinterfaces >=2 and not self.net2:
            raise ValidationError("net2 is required")
        if self.numinterfaces >=1 and not self.subnet1:
            raise ValidationError("Subnet1 is required")
        if self.numinterfaces >=2 and not self.subnet2:
            raise ValidationError("Subnet2 is required")
        if self.foreman and not self.dns:
            raise ValidationError("Foreman requires a DNS domain to be set")
        if self.foreman and not self.foremanprovider:
            raise ValidationError("Foreman requires a ForemanProvider to be set")
        if self.foremanparameters and not self.foreman:
            raise ValidationError("Foreman Parameters requires foreman to be set")
        if self.cobbler and not self.cobblerprovider:
            raise ValidationError("Cobbler requires a CobblerProvider to be set")
        if self.cobblerparameters and not self.cobbler:
            raise ValidationError("Cobbler Parameters requires Cobbler to be set")
        if not self.physicalprovider and not self.virtualprovider:
            raise ValidationError("You need to assign at least one physical or virtual provider")
        if self.cloudinit and not self.rootpw:
            raise ValidationError("Cloudinit requires a rootpw to be set")
        if self.cobbler and self.cobblerprovider:
            cobblerprovider = self.cobblerprovider
            connection=checkconn(cobblerprovider.host,COBBLERPORT)
            if not connection:
                raise ValidationError("Cobbler server cant be reached...")
            cobblerprofile = self.name
            if self.cobblerprofile:
                cobblerprofile = self.cobblerprofile
            cobbler=Cobbler(cobblerprovider.host, cobblerprovider.user, cobblerprovider.password)
            profilefound = cobbler.checkprofile(cobblerprofile)
            if not profilefound:
                raise ValidationError("Invalid cobbler profile")
        if self.virtualprovider:
            virtualprovider = self.virtualprovider
            if virtualprovider.type == 'ovirt':
                ovirt=Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
                clusterfound = ovirt.checkcluster(self.clu)
                if not clusterfound:
                    raise ValidationError("Invalid Cluster")
                if self.numinterfaces >= 1:
                    net1found = ovirt.checknetwork(self.clu,self.net1)
                    if not net1found:
                        raise ValidationError("Invalid net1")
                if self.numinterfaces >= 2:
                    net2found = ovirt.checknetwork(self.clu,self.net2)
                    if not net2found:
                        raise ValidationError("Invalid net2")
                if self.template != '':
                    templates = ovirt.gettemplates()
                    if self.template not in templates:
                        raise ValidationError("Invalid template. Use of the following ones:%s" % (','.join(templates) ) )
            if virtualprovider.type == 'vsphere':
                gettemplatescommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (settings.PWD, 'gettemplates', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu)
                gettemplatescommand = os.popen(gettemplatescommand).read()
                templates = ast.literal_eval(gettemplatescommand)
                if self.template not in templates:
                    raise ValidationError("Invalid template. Use of the following ones:%s" % (','.join(templates) ) )
    class Meta:
        ordering  = ['name']


class VM(models.Model):
    name              = models.CharField(max_length=80)
    storagedomain     = models.CharField(max_length=80,blank=True,null=True)
    physicalprovider  = models.ForeignKey(PhysicalProvider,blank=True,null=True)
    virtualprovider   = models.ForeignKey(VirtualProvider,blank=True,null=True)
    physical          = models.BooleanField(default=False)
    cobblerprovider   = models.ForeignKey(CobblerProvider, blank=True,null=True)
    foremanprovider   = models.ForeignKey(ForemanProvider,blank=True,null=True)
    profile           = models.ForeignKey(Profile)
    ip1               = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    mac1              = models.CharField(max_length=20, blank=True,null=True)
    ip2               = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    mac2              = models.CharField(max_length=20, blank=True,null=True)
    ip3               = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    mac3              = models.CharField(max_length=20,blank=True,null=True)
    ip4               = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
    mac4              = models.CharField(max_length=20, blank=True,null=True)
    ipilo             = models.CharField(max_length=60,blank=True, null=True)
    ipoa              = models.CharField(max_length=60,blank=True, null=True)
    iso               = models.CharField(max_length=100, default='',choices=( ('xx', '') , ('yy' , '') ))
    hostgroup         = models.CharField(max_length=30, default='',choices=( ('xx', '') , ('yy' , '') ))
    puppetclasses     = models.CharField(max_length=30, null=True,default='',choices=( ('xx', '') , ('yy' , '') ))
    parameters        = models.TextField(blank=True)
    createdby         = models.ForeignKey(User,default=1,blank=True)
    createdwhen       = models.DateTimeField(editable=True,blank=True,null=True)
    price             = models.IntegerField(blank=True,null=True)
    unmanaged         = models.BooleanField(default=False)
    status            = models.CharField(max_length=20, default='N/A')
    create            = models.BooleanField(default=True)
    def __unicode__(self):
        if self.virtualprovider:
            return "%s : %s" % (self.virtualprovider.name,self.name)
        else:
            return "physical:%s" % (self.name)
    def save(self, *args, **kwargs):
        if self.pk:
            super(VM, self).save(*args, **kwargs)
            return
        self.createdwhen=datetime.now()
        name, storagedomain, physicalprovider, virtualprovider, physical, cobblerprovider, foremanprovider, profile, ip1, mac1, ip2, mac2, ip3, mac3, ip4, mac4, puppetclasses, parameters, createdby, iso, ipilo, ipoa, hostgroup, createdwhen, price, unmanaged, status, create = self.name, self.storagedomain, self.physicalprovider, self.virtualprovider, self.physical, self.cobblerprovider, self.foremanprovider, self.profile, self.ip1, self.mac1, self.ip2, self.mac2, self.ip3, self.mac3, self.ip4, self.mac4, self.puppetclasses, self.parameters, self.createdby, self.iso, self.ipilo, self.ipoa, self.hostgroup, self.createdwhen, self.price, self.unmanaged, self.status, self.create
        clu, guestid, memory, numcpu, disksize1, diskthin1, disksize2, diskthin2, diskinterface, numinterfaces, net1, subnet1, net2, subnet2, net3, subnet3, net4, subnet4, netinterface, dns, foreman, cobbler, foremanparameters, cobblerparameters, vnc , nextserver, template, cloudinit, rootpw, dns1 = profile.clu, profile.guestid, profile.memory, profile.numcpu, profile.disksize1, profile.diskthin1, profile.disksize2, profile.diskthin2, profile.diskinterface, profile.numinterfaces, profile.net1, profile.subnet1, profile.net2, profile.subnet2, profile.net3, profile.subnet3, profile.net4, profile.subnet4, profile.netinterface, profile.dns, profile.foreman, profile.cobbler, profile.foremanparameters, profile.cobblerparameters, profile.vnc, profile.nextserver, profile.template, profile.cloudinit, profile.rootpw, profile.dns1
        beforecreate, aftercreate, beforestart, afterstart, afterbuild = profile.hookbeforecreate, profile.hookaftercreate, profile.hookbeforestart, profile.hookafterstart, profile.hookafterbuild
        if beforecreate:
            env = os.environ
            env['vm_name'], env['vm_storagedomain'], env['vm_physicalprovider'], env['vm_virtualprovider'], env['vm_physical'], env['vm_cobblerprovider'], env['vm_foremanprovider'], env['vm_profile'], env['vm_ip1'], env['vm_mac1'], env['vm_ip2'], env['vm_mac2'], env['vm_ip3'], env['vm_mac3'], env['vm_ip4'], env['vm_mac4'], env['vm_ipilo'], env['vm_ipoa'], env['vm_iso'], env['vm_hostgroup'], env['vm_puppetclasses'], env['vm_parameters'], env['vm_createdby'], env['vm_createdwhen'], env['vm_price'], env['vm_unmanaged'], env['vm_status'], env['vm_create'] = name, nonone(storagedomain), nonone(physicalprovider), nonone(virtualprovider), nonone(physical), nonone(cobblerprovider), nonone(foremanprovider), nonone(profile), nonone(ip1), nonone(mac1), nonone(ip2), nonone(mac2), nonone(ip3), nonone(mac3), nonone(ip4), nonone(mac4), nonone(ipilo), nonone(ipoa), nonone(iso), nonone(hostgroup), nonone(puppetclasses), nonone(parameters), nonone(createdby), nonone(createdwhen), nonone(price), nonone(unmanaged), nonone(status), nonone(create)
            env['vm_mail'] = createdby.email
            scriptpath  = "%s/%s" % (hooks, beforecreate.name)
            interpreter = beforecreate.type
            if not os.path.exists(scriptpath):
                content = beforecreate.content
                f = open(scriptpath)
                f.write(content)
                f.close()
            subprocess.Popen("%s %s" % (interpreter, scriptpath), stdout=subprocess.PIPE, shell=True, env=env).stdout.read()
        if profile.price:
            self.price = profile.price
        if profile.ipamprovider:
            ipamprovider=profile.ipamprovider
            connection=checkconn(ipamprovider.host,ipamprovider.port)
            if not connection:
                return "Connectivity issue with Ipam %s!" % ipamprovider.host
            #TODO: RETRIEVE IPS (AND NAME?)
        if physical:
            physicalprovider = profile.physicalprovider
            if physicalprovider.type == 'oa':
                connection=checkconn(ipoa,22)
            elif physicalprovider.type == 'ilo':
                connection=checkconn(ipilo,22)
        elif create:
            connection=checkconn(virtualprovider.host,virtualprovider.port)
            if not connection:
                return "Connectivity issue with virtual provider %s!" % virtualprovider.name
        if cobbler and cobblerprovider:
            connection = checkconn(cobblerprovider.host, COBBLERPORT)
            if not connection:
                return "Connectivity issue with cobbler provider %s!" % cobblerprovider.name
            cobblerhost, cobbleruser, cobblerpassword = cobblerprovider.host, cobblerprovider.user, cobblerprovider.password
            cobbler=Cobbler(cobblerhost, cobbleruser, cobblerpassword)
            cobblerfound = cobbler.exists(name)
            if cobblerfound:
                return "Machine %s allready exists within cobbler!" % name
        if foreman and foremanprovider:
            connection = checkconn(foremanprovider.host, foremanprovider.port)
            if not connection:
                return "Connectivity issue with foreman provider %s!" % foremanprovider.name
            foremanhost, foremanport, foremansecure, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port, foremanprovider.secure, foremanprovider.user, foremanprovider.password
            foreman=Foreman(host=foremanhost,port=foremanport, user=foremanuser, password=foremanpassword, secure=foremansecure)
            foremanfound = foreman.exists(name, dns)
            if foremanfound:
                return "Machine %s.%s allready exists within foreman!" % (name,dns)

        cmdline="user=%s" % (createdby.username)
        if profile.cmdline:
            cmdline="%s %s" % (profile.cmdline,cmdline)
        if physical :
            cmdline="%s blacklist=lpfc blacklist=qla2xxx blacklist=qla4xxx" % (cmdline)
        if physical and profile.console:
            cmdline="%s console=ttyS0" % (cmdline)
        #VM CREATION
        if not physical and create and virtualprovider.type == 'ovirt':
            ovirt=Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
            if template:
                ovirt.createfromtemplate(name,template)
                ovirt.macaddr = ovirt.getmacs(name)
            else:
                ovirt.create(name=name, clu=clu, numcpu=numcpu, numinterfaces=numinterfaces, netinterface=netinterface, disksize1=disksize1,diskthin1=diskthin1, disksize2=disksize2,diskthin2=diskthin2, diskinterface=diskinterface, memory=memory, storagedomain=storagedomain, guestid=guestid, net1=net1, net2=net2, net3=net3, net4=net4, mac1=mac1, mac2=mac2, iso=iso, vnc=vnc)
            ovirt.close()
        if not physical and create and virtualprovider.type == 'kvirt':
            kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
            kvirt.create(name=name, clu=clu, numcpu=numcpu, numinterfaces=numinterfaces, netinterface=netinterface, disksize1=disksize1,diskthin1=diskthin1, disksize2=disksize2,diskthin2=diskthin2, diskinterface=diskinterface, memory=memory, storagedomain=storagedomain, guestid=guestid, net1=net1, net2=net2, net3=net3, net4=net4, mac1=mac1, mac2=mac2, iso=iso, vnc=vnc)
            kvirt.close()
        if not physical and create and virtualprovider.type == 'vsphere':
            if template:
                createfromtemplatecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s %s" % (settings.PWD,'createfromtemplate', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu , name, template)
                createfromtemplatecommand = os.popen(createfromtemplatecommand).read()
                getmacscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (settings.PWD,'getmacs', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu , name)
                vspheremacaddr = os.popen(getmacscommand).read()
                vspheremacaddr = ast.literal_eval(vspheremacaddr)
            else:
                createcommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s \'%s' '%s' '%s' '%s' '%s' '%s' '%s' '%s'" % (settings.PWD,'create', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu , name, numcpu, numinterfaces,  disksize1 , diskthin1, disksize2 , diskthin2, storagedomain, memory, guestid, vnc, iso, net1, net2, net3, net4)
                vspheremacaddr = os.popen(createcommand).read()
                vspheremacaddr = ast.literal_eval(vspheremacaddr)
        if cobbler and cobblerprovider:
            if not physical and create and virtualprovider.type == 'ovirt':
                macaddr=ovirt.macaddr
            if not physical and create and virtualprovider.type == 'kvirt':
                macaddr=kvirt.macaddr
            if not physical and create and virtualprovider.type == 'vsphere':
                macaddr=vspheremacaddr
            if not physical and virtualprovider.type == 'fake':
                if mac1:
                    macaddr=[mac1]
                else:
                    macaddr=['11:11:11:11:11:11']
            if physical:
                macaddr=[mac1]
                if mac2:
                    macaddr.append(mac2)
            if not create:
                macaddr=[mac1]
                if mac2:
                    macaddr.append(mac2)
                if mac3:
                    macaddr.append(mac3)
                if mac4:
                    macaddr.append(mac4)
            cobblerprofile=profile.name
            if profile.cobblerprofile:
                cobblerprofile=profile.cobblerprofile
            cobblerhost, cobbleruser, cobblerpassword = cobblerprovider.host, cobblerprovider.user, cobblerprovider.password
            cobbler=Cobbler(cobblerhost, cobbleruser, cobblerpassword)
            if cobblerparameters:
                cobblerparameters = parameters
            if ip1:
                cobbler.create(name=name, profile=cobblerprofile, numinterfaces=numinterfaces, dns=dns, ip1=ip1, subnet1=subnet1, ip2=ip2, subnet2=subnet2, ip3=ip3, subnet3=subnet3, ip4=ip4, subnet4=subnet4, macaddr=macaddr, parameters=cobblerparameters,cmdline=cmdline, nextserver=nextserver)
            else:
                cobbler.simplecreate(name=name, profile=cobblerprofile, numinterfaces=numinterfaces, dns=dns, macaddr=macaddr, parameters=cobblerparameters,cmdline=cmdline, nextserver=nextserver)
        if foreman and foremanprovider:
            foremanhost, foremanport, foremansecure, foremanuser, foremanpassword, foremanos, foremanenv, foremanarch, foremanpuppet, foremanptable = foremanprovider.host, foremanprovider.port, foremanprovider.secure, foremanprovider.user, foremanprovider.password, foremanprovider.osid, foremanprovider.envid, foremanprovider.archid, foremanprovider.puppetid, foremanprovider.ptableid
            f=Foreman(host=foremanhost, port=foremanport,user=foremanuser, password=foremanpassword, secure=foremansecure)
            f.create(name=name,dns=dns,ip=ip1,hostgroup=hostgroup)
            if foremanparameters and parameters != '':
                f.addparameters(name=name,dns=dns,parameters=parameters)
        super(VM, self).save(*args, **kwargs)
        if aftercreate:
            env = os.environ
            env['vm_name'], env['vm_storagedomain'], env['vm_physicalprovider'], env['vm_virtualprovider'], env['vm_physical'], env['vm_cobblerprovider'], env['vm_foremanprovider'], env['vm_profile'], env['vm_ip1'], env['vm_mac1'], env['vm_ip2'], env['vm_mac2'], env['vm_ip3'], env['vm_mac3'], env['vm_ip4'], env['vm_mac4'], env['vm_ipilo'], env['vm_ipoa'], env['vm_iso'], env['vm_hostgroup'], env['vm_puppetclasses'], env['vm_parameters'], env['vm_createdby'], env['vm_createdwhen'], env['vm_price'], env['vm_unmanaged'], env['vm_status'], env['vm_create'] = name, nonone(storagedomain), nonone(physicalprovider), nonone(virtualprovider), nonone(physical), nonone(cobblerprovider), nonone(foremanprovider), nonone(profile), nonone(ip1), nonone(mac1), nonone(ip2), nonone(mac2), nonone(ip3), nonone(mac3), nonone(ip4), nonone(mac4), nonone(ipilo), nonone(ipoa), nonone(iso), nonone(hostgroup), nonone(puppetclasses), nonone(parameters), nonone(createdby), nonone(createdwhen), nonone(price), nonone(unmanaged), nonone(status), nonone(create)
            env['vm_mail'] = createdby.email
            scriptpath  = "%s/%s" % (hooks, aftercreate.name)
            interpreter = aftercreate.type
            if not os.path.exists(scriptpath):
                content = aftercreate.content
                f = open(scriptpath)
                f.write(content)
                f.close()
            subprocess.Popen("%s %s" % (interpreter, scriptpath), stdout=subprocess.PIPE, shell=True, env=env).stdout.read()
        if beforestart:
            env = os.environ
            env['vm_name'], env['vm_storagedomain'], env['vm_physicalprovider'], env['vm_virtualprovider'], env['vm_physical'], env['vm_cobblerprovider'], env['vm_foremanprovider'], env['vm_profile'], env['vm_ip1'], env['vm_mac1'], env['vm_ip2'], env['vm_mac2'], env['vm_ip3'], env['vm_mac3'], env['vm_ip4'], env['vm_mac4'], env['vm_ipilo'], env['vm_ipoa'], env['vm_iso'], env['vm_hostgroup'], env['vm_puppetclasses'], env['vm_parameters'], env['vm_createdby'], env['vm_createdwhen'], env['vm_price'], env['vm_unmanaged'], env['vm_status'], env['vm_create'] = name, nonone(storagedomain), nonone(physicalprovider), nonone(virtualprovider), nonone(physical), nonone(cobblerprovider), nonone(foremanprovider), nonone(profile), nonone(ip1), nonone(mac1), nonone(ip2), nonone(mac2), nonone(ip3), nonone(mac3), nonone(ip4), nonone(mac4), nonone(ipilo), nonone(ipoa), nonone(iso), nonone(hostgroup), nonone(puppetclasses), nonone(parameters), nonone(createdby), nonone(createdwhen), nonone(price), nonone(unmanaged), nonone(status), nonone(create)
            env['vm_mail'] = createdby.email
            scriptpath  = "%s/%s" % (hooks, beforestart.name)
            interpreter = beforestart.type
            if not os.path.exists(scriptpath):
                content = beforestart.content
                f = open(scriptpath)
                f.write(content)
                f.close()
            subprocess.Popen("%s %s" % (interpreter, scriptpath), stdout=subprocess.PIPE, shell=True, env=env).stdout.read()
        if physical and physicalprovider.type == 'ilo':
            ilo=Ilo(ipilo,physicalprovider.user,physicalprovider.password)
            ilo.pxe()
            ilo.reset()
        if physical and physicalprovider.type == 'oa':
            oa=Oa(ipoa,physicalprovider.user,physicalprovider.password)
            bladeid = oa.getid(name)
            status = oa.status(bladeid)
            if status == 'up':
                oa.rebootpxe(bladeid)
            else:
                oa.startpxe(bladeid)
        if not physical and create and virtualprovider.type == 'ovirt':
            ovirt=Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
            if cloudinit:
                ovirt.cloudinit(name, numinterfaces=numinterfaces, ip1=ip1, subnet1=subnet1, ip2=ip2, subnet2=subnet2, ip3=ip3, subnet3=subnet3, ip4=ip4, subnet4=subnet4, rootpw=rootpw, dns=dns1, dns1=dns1)
            else:
                ovirt.start(name)
            ovirt.close()
        if not physical and create and virtualprovider.type == 'kvirt':
            kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
            kvirt.start(name)
            kvirt.close()
        if not physical and create and virtualprovider.type == 'vsphere':
            startcommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (settings.PWD,'start', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
            os.popen(startcommand).read()
        if afterstart:
            env = os.environ
            env['vm_name'], env['vm_storagedomain'], env['vm_physicalprovider'], env['vm_virtualprovider'], env['vm_physical'], env['vm_cobblerprovider'], env['vm_foremanprovider'], env['vm_profile'], env['vm_ip1'], env['vm_mac1'], env['vm_ip2'], env['vm_mac2'], env['vm_ip3'], env['vm_mac3'], env['vm_ip4'], env['vm_mac4'], env['vm_ipilo'], env['vm_ipoa'], env['vm_iso'], env['vm_hostgroup'], env['vm_puppetclasses'], env['vm_parameters'], env['vm_createdby'], env['vm_createdwhen'], env['vm_price'], env['vm_unmanaged'], env['vm_status'], env['vm_create'] = name, nonone(storagedomain), nonone(physicalprovider), nonone(virtualprovider), nonone(physical), nonone(cobblerprovider), nonone(foremanprovider), nonone(profile), nonone(ip1), nonone(mac1), nonone(ip2), nonone(mac2), nonone(ip3), nonone(mac3), nonone(ip4), nonone(mac4), nonone(ipilo), nonone(ipoa), nonone(iso), nonone(hostgroup), nonone(puppetclasses), nonone(parameters), nonone(createdby), nonone(createdwhen), nonone(price), nonone(unmanaged), nonone(status), nonone(create)
            env['vm_mail'] = createdby.email
            scriptpath  = "%s/%s" % (hooks, afterstart.name)
            interpreter = afterstart.type
            if not os.path.exists(scriptpath):
                content = afterstart.content
                f = open(scriptpath)
                f.write(content)
                f.close()
            subprocess.Popen("%s %s" % (interpreter, scriptpath), stdout=subprocess.PIPE, shell=True, env=env).stdout.read()
        return 'OK'

class Default(models.Model):
    name              = models.CharField(max_length=20)
    virtualprovider   = models.ForeignKey(VirtualProvider,blank=True,null=True)
    cobblerprovider   = models.ForeignKey(CobblerProvider,blank=True,null=True)
    foremanprovider   = models.ForeignKey(ForemanProvider,blank=True,null=True)
    consoleip         = models.CharField(max_length=60,blank=True, null=True)
    consoleport       = models.IntegerField(default=443)
    consolesecure     = models.BooleanField(default=False)
    consoleminport    = models.IntegerField(default=6000)
    consolemaxport    = models.IntegerField(default=7000)
    currency          = models.CharField(max_length=20, default='$',choices=( ('$', '$'),('€', '€') ))
#    color             = models.CharField(max_length=7,default='#ADD8E6')
    def __unicode__(self):
        return self.name
    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError("Can only create 1 %s instance" % model.__name__)
#    def save(self, *args, **kw):
#        if self.pk is not None:
#            ori = Default.objects.get(pk=self.pk)
#            if ori.color != self.color:
#                content=""".navbar-inner
#                {
#                            background-color: %s;
#                                background-image: none;
#                                }   
#
#                .dropdown-menu
#                {
#                            background-color: %s;
#                                background-image: none;
#                                }""" % (self.color, self.color)
#                colorfile = open("%s/static/css/colors.custom.css" % settings.PWD , 'w')
#                colorfile.write(content)
#                colorfile.close()
#
#        super(Default, self).save(*args, **kw)
