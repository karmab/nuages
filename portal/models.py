# -*- coding: iso-8859-15 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User,Group
import ast
import hashlib
import os
import random
import requests
import subprocess
import time
import django.utils.simplejson as json
import datetime
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from nuages.settings import LOGIN_REDIRECT_URL as baseurl
hooks = settings.PWD+'/hooks'
import logging


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
try:
    from portal.ilo import Ilo
except:
    print "Missing python-paramiko package for ilo support"
try:
    from portal.oa import Oa
except:
    print "Missing python-paramiko package for oa support"
import socket


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

def vmstart(name,virtualprovider):
    if virtualprovider.type == 'ovirt':
        ovirt   = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
        results = ovirt.start(name)
        ovirt.close()
    elif virtualprovider.type == 'kvirt':
        kvirt   = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
        results = kvirt.start(name)
        kvirt.close()
    elif virtualprovider.type == 'vsphere':
        startcommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (settings.PWD,'start', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
        startinfo    = os.popen(startcommand).read()
        results      = json.dumps(startinfo)
    return results

def vmstop(name,virtualprovider):
    if virtualprovider.type == 'ovirt':
        ovirt   = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
        results = ovirt.stop(name)
        ovirt.close()
    elif virtualprovider.type == 'kvirt':
        kvirt   = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
        results = kvirt.stop(name)
        kvirt.close()
    elif virtualprovider.type == 'vsphere':
        stopcommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (settings.PWD,'stop', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu , name )
        stopinfo    = os.popen(stopcommand).read()
        results     = json.dumps(stopinfo)
    return results

def vmremove(name,virtualprovider):
    if virtualprovider and virtualprovider.type == 'ovirt':
        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
        ovirt.remove(name)
        ovirt.close()
    elif virtualprovider and virtualprovider.type == 'kvirt':
        kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
        kvirt.remove(name)
        kvirt.close()
    elif virtualprovider and virtualprovider.type == 'vsphere':
        removecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (settings.PWD,'remove', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu , name )
        os.popen(removecommand).read()

def vmstatus(name,virtualprovider):
    if virtualprovider.type == 'ovirt':
        ovirt   = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
        results = ovirt.status(name)
        ovirt.close()
    elif virtualprovider.type == 'kvirt':
        kvirt   = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
        results = kvirt.status(name)
        kvirt.close()
    elif virtualprovider.type == 'vsphere':
        statuscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (settings.PWD,'status', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
        statusinfo    = os.popen(statuscommand).read()
        results      = json.dumps(statusinfo)
    return results

def internalname(profile):
    naming = profile.ipamprovider.naming
    names = VM.objects.filter(profile=profile).filter(name__startswith=naming).values('name')
    if names == None:
        name = "%s001" % (naming)
    else:
        counter = 0
        for n in names:
            if int(n['name'][-3:])> counter:
                counter = int(n['name'][-3:])
        counter = counter+1
        name = "%s%0.3d"  % (naming, counter)
        return name

def marvelname(profile):
    ipamprovider  = profile.ipamprovider
    pubkey        = ipamprovider.pubkey
    privkey       = ipamprovider.privkey
    timestamp     = str(int(time.time()))
    offset        = random.randrange(1,1402)
    limit         = '1'
    hashvalue     = hashlib.md5(timestamp + privkey + pubkey).hexdigest()
    uri           = "http://gateway.marvel.com:80/v1/public/characters?limit=%s&offset=%s&apikey=%s&ts=%s&hash=%s" % (limit, offset, pubkey, timestamp, hashvalue)
    headers       = {'content-type':'application/json'}
    request       = requests.get(uri, headers=headers)
    data          = json.loads(request.content)
    name          = data['data']['results'][0]['name'].strip().split(' ')[0]
    return name

def internalip(profile,index):
    netranges = { 1: profile.ipamprovider.range1, 2: profile.ipamprovider.range2, 3 : profile.ipamprovider.range3 , 4: profile.ipamprovider.range4 }
    netrange = netranges[index]
    if netrange == '':
        return ''
    filter = "ip%d" % index
    if index == 1:
        ips = VM.objects.filter(profile=profile).exclude(ip1=None).values('ip1')
    elif index == 2:
        ips = VM.objects.filter(profile=profile).exclude(ip2=None).values('ip2')
    elif index == 3:
        ips = VM.objects.filter(profile=profile).exclude(ip3=None).values('ip3')
    elif index == 4:
        ips = VM.objects.filter(profile=profile).exclude(ip4=None).values('ip4')
    last = 0
    for i in ips:
        ip = i[filter]
        currentlast = int(ip.split('.')[3])
        if ip.startswith(netrange) and currentlast > last:
            last = currentlast
    last = last+1
    return "%s.%d" % (netrange, last)

class IpamProvider(models.Model):
    name                = models.CharField(max_length=80)
    type                = models.CharField(max_length=20, default='internal',choices=( ('internal', 'internal'),('marvel', 'marvel') ))
    #host                = models.CharField(max_length=60, blank=True, null=True)
    #port                = models.IntegerField(default=80, blank=True, null=True)
    #user                = models.CharField(max_length=60, blank=True, null=True)
    #password            = models.CharField(max_length=20, blank=True, null=True)
    privkey             = models.CharField(max_length=100, blank=True, null=True)
    pubkey              = models.CharField(max_length=100, blank=True, null=True)
    naming              = models.CharField(max_length=80, blank=True, null=True)
    range1              = models.CharField(max_length=40, blank=True, null=True)
    range1              = models.CharField(max_length=40, blank=True, null=True)
    range2              = models.CharField(max_length=40, blank=True, null=True)
    range3              = models.CharField(max_length=40, blank=True, null=True)
    range4              = models.CharField(max_length=40, blank=True, null=True)
    def __unicode__(self):
        return self.name
    def clean(self):
        if self.type == 'internal' and not self.naming:
                raise ValidationError("Internal needs naming")
        if self.type == 'marvel'  and not self.privkey:
                raise ValidationError("Marvel needs priv key")
        if self.type == 'marvel'  and not self.pubkey:
                raise ValidationError("Marvel needs pub key")
        if self.type == 'internal'  and not self.naming:
                raise ValidationError("Internal needs naming to be set")

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
    def storage(self):
        if self.type == 'ovirt':
            ovirt = Ovirt(self.host, self.port, self.user, self.password, self.ssl)
            storageinfo = ovirt.getstorage()
            ovirt.close()
        elif self.type == 'kvirt':
            kvirt = Kvirt(self.host,self.port,self.user,protocol='ssh')
            storageinfo = kvirt.getstorage()
            kvirt.close()
        elif self.type == 'vsphere':
            jythoncommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (settings.PWD, 'getstorage', self.host, self.user, self.password , self.datacenter, self.clu )
            storageinfo = os.popen(jythoncommand).read()
        return storageinfo
    
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
    ptableid            = models.CharField(max_length=20, blank=True, null=True)
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
    datacenter        = models.CharField(max_length=50,blank=True,null=True)
    template          = models.CharField(max_length=80,blank=True,null=True)
    clu               = models.CharField(max_length=50,blank=True)
    guestid           = models.CharField(max_length=20,default='rhel_6x64', choices=( ('rhel_6x64', 'rhel_6x64'),('rhel_5x64', 'rhel_5x64'),('windows_xp', 'windows_xp') ))
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
    gateway           = models.GenericIPAddressField(blank=True, null=True, protocol="IPv4")
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
    foremanenv        = models.CharField(max_length=40, blank=True)
    cobbler           = models.BooleanField(default=False)
    cobblerparameters = models.BooleanField(default=False)
    iso               = models.BooleanField(default=False)
    hide              = models.BooleanField(default=True)
    console           = models.BooleanField(default=False)
    requireip         = models.BooleanField(default=False)
    deletable         = models.BooleanField(default=True)
    fulldelete        = models.BooleanField(default=True)
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
                if self.template != '':
                    gettemplatescommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (settings.PWD, 'gettemplates', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu)
                    gettemplatescommand = os.popen(gettemplatescommand).read()
                    templates = ast.literal_eval(gettemplatescommand)
                    if self.template not in templates:
                        raise ValidationError("Invalid template. Use of the following ones:%s" % (','.join(templates) ) )
        if self.fulldelete and not self.deletable:
            raise ValidationError("Full delete requires deletable to be set")
    class Meta:
        ordering  = ['name']


class VM(models.Model):
    name              = models.CharField(max_length=80)
    storagedomain     = models.CharField(max_length=80,blank=True,null=True)
    physical          = models.BooleanField(default=False)
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
        if self.profile.virtualprovider:
            return "%s : %s" % (self.profile.virtualprovider.name,self.name)
        else:
            return "physical:%s" % (self.name)
    def save(self, *args, **kwargs):
        logging.debug('prout')
        if self.pk:
            super(VM, self).save(*args, **kwargs)
            return
        #self.createdwhen = datetime.now()
        self.createdwhen = timezone.now()
        name, storagedomain, physical, profile, ip1, mac1, ip2, mac2, ip3, mac3, ip4, mac4, puppetclasses, parameters, createdby, iso, ipilo, ipoa, hostgroup, createdwhen, price, unmanaged, status, create = self.name, self.storagedomain, self.physical, self.profile, self.ip1, self.mac1, self.ip2, self.mac2, self.ip3, self.mac3, self.ip4, self.mac4, self.puppetclasses, self.parameters, self.createdby, self.iso, self.ipilo, self.ipoa, self.hostgroup, self.createdwhen, self.price, self.unmanaged, self.status, self.create
        physicalprovider, virtualprovider, cobblerprovider, foremanprovider, ipamprovider = profile.physicalprovider, profile.virtualprovider, profile.cobblerprovider, profile.foremanprovider, profile.ipamprovider
        clu, guestid, memory, numcpu, disksize1, diskthin1, disksize2, diskthin2, diskinterface, numinterfaces, net1, subnet1, net2, subnet2, net3, subnet3, net4, subnet4, gateway, netinterface, dns, foreman, cobbler, foremanparameters, cobblerparameters, vnc , nextserver, template, cloudinit, rootpw, dns1, requireip = profile.clu, profile.guestid, profile.memory, profile.numcpu, profile.disksize1, profile.diskthin1, profile.disksize2, profile.diskthin2, profile.diskinterface, profile.numinterfaces, profile.net1, profile.subnet1, profile.net2, profile.subnet2, profile.net3, profile.subnet3, profile.net4, profile.subnet4, profile.gateway, profile.netinterface, profile.dns, profile.foreman, profile.cobbler, profile.foremanparameters, profile.cobblerparameters, profile.vnc, profile.nextserver, profile.template, profile.cloudinit, profile.rootpw, profile.dns1, profile.requireip
        if storagedomain == None and profile.autostorage:
            #RETRIEVE BEST STORAGE DOMAIN
            if virtualprovider.type == 'ovirt':
                ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
                beststorage = ovirt.beststorage(virtualprovider.datacenter)
                ovirt.close()
            elif virtualprovider.type == 'kvirt':
                kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
                beststorage = kvirt.beststorage()
                kvirt.close()
            elif virtualprovider.type == 'vsphere':
                beststoragecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (settings.PWD,'beststorage', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu)
                bestds = os.popen(beststoragecommand).read()
                beststorage=bestds.strip()
                self.storagedomain = beststorage
                storagedomain = self.storagedomain
        beforecreate, aftercreate, beforestart, afterstart, afterbuild = profile.hookbeforecreate, profile.hookaftercreate, profile.hookbeforestart, profile.hookafterstart, profile.hookafterbuild
        if name == '':
            if not ipamprovider:
                return "Setting a name is required!"
            elif ipamprovider.type == 'internal':
                self.name = internalname(profile)
            elif ipamprovider.type == 'marvel':
                new = False
                while not new:
                    newname = marvelname(profile).lower()
                    print "Using %s from marvel" % newname
                    if len(VM.objects.filter(name=newname)) == 0:
                        new = True
                self.name = newname
        name      = self.name
        if ip1 == '' and ipamprovider:
            if ipamprovider.type == 'internal':
                self.ip1 = internalip(profile, 1)
                ip1      = self.ip1
        if ip2 == '' and ipamprovider and numinterfaces >1:
            if ipamprovider.type == 'internal':
                self.ip2 = internalip(profile, 2)
                ip2      = self.ip2
        if ip3 == '' and ipamprovider and numinterfaces >2:
            if ipamprovider.type == 'internal':
                self.ip3 = internalip(profile, 3)
                ip3      = self.ip3
        if ip4 == '' and ipamprovider and numinterfaces >3:
            if ipamprovider.type == 'internal':
                self.ip4 = internalip(profile, 4)
                ip4      = self.ip4
        if requireip and ip1 == '':
                return "Setting ip1 is required!"
        if requireip and ip2 == '' and numinterfaces >1:
                return "Setting ip2 is required!"
        if requireip and ip3 == '' and numinterfaces >2:
                return "Setting ip3 is required!"
        if requireip and ip4 == '' and numinterfaces >3:
                return "Setting ip4 is required!"
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
                cobbler.create(name=name, profile=cobblerprofile, numinterfaces=numinterfaces, dns=dns, ip1=ip1, subnet1=subnet1, ip2=ip2, subnet2=subnet2, ip3=ip3, subnet3=subnet3, ip4=ip4, subnet4=subnet4, gateway=gateway, macaddr=macaddr, parameters=cobblerparameters,cmdline=cmdline, nextserver=nextserver)
            else:
                cobbler.simplecreate(name=name, profile=cobblerprofile, numinterfaces=numinterfaces, dns=dns, macaddr=macaddr, parameters=cobblerparameters,cmdline=cmdline, nextserver=nextserver)
        if foreman and foremanprovider:
            foremanhost, foremanport, foremansecure, foremanuser, foremanpassword, foremanos, foremanenv, foremanarch, foremanpuppet, foremanptable = foremanprovider.host, foremanprovider.port, foremanprovider.secure, foremanprovider.user, foremanprovider.password, foremanprovider.osid, foremanprovider.envid, foremanprovider.archid, foremanprovider.puppetid, foremanprovider.ptableid
            f=Foreman(host=foremanhost, port=foremanport,user=foremanuser, password=foremanpassword, secure=foremansecure)
            if profile.foremanenv:
                environment = profile.foremanenv
            f.create(name=name, dns=dns, ip=ip1, hostgroup=hostgroup, environment=environment)
            if puppetclasses != '':
                f.addclasses(name=name, dns=dns, classes=puppetclasses)
            if foremanparameters and parameters != '':
                f.addparameters(name=name, dns=dns, parameters=parameters)
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
                ovirt.cloudinit(name, numinterfaces=numinterfaces, ip1=ip1, subnet1=subnet1, ip2=ip2, subnet2=subnet2, ip3=ip3, subnet3=subnet3, ip4=ip4, subnet4=subnet4, gateway=gateway, rootpw=rootpw, dns=dns1, dns1=dns1)
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
    def kill(self, *args, **kwargs):
        name = self.name
        virtualprovider = self.profile.virtualprovider
        cobblerprovider = self.profile.cobblerprovider
        foremanprovider = self.profile.foremanprovider
        if cobblerprovider:
            cobblerhost, cobbleruser, cobblerpassword = cobblerprovider.host, cobblerprovider.user, cobblerprovider.password
            cobbler = Cobbler(cobblerhost, cobbleruser, cobblerpassword)
            cobbler.remove(name)
        if foremanprovider:
            dns = self.profile.dns
            foremanhost, foremanport, foremansecure, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port,foremanprovider.secure, foremanprovider.user, foremanprovider.password
            foreman = Foreman(host=foremanhost,port=foremanport,user=foremanuser, password=foremanpassword, secure=foremansecure)
            foreman.delete(name=name, dns=dns)
        vmremove(name, virtualprovider)
    def console(self, *args, **kwargs):
        results   = "%s/vms/console/?id=%s" % ( baseurl, self.id)
        return  results
    def start(self, *args, **kwargs):
        name            = self.name
        virtualprovider = self.profile.virtualprovider
        return vmstart(name, virtualprovider)
    def stop(self, *args, **kwargs):
        name            = self.name
        virtualprovider = self.profile.virtualprovider
        return vmstop(name, virtualprovider)
    def status(self, *args, **kwargs):
        name            = self.name
        virtualprovider = self.profile.virtualprovider
        return vmstatus(name, virtualprovider)

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
    def __unicode__(self):
        return self.name
    def clean(self):
        model = self.__class__
        if (model.objects.count() > 0 and self.id != model.objects.get().id):
            raise ValidationError("Can only create 1 %s instance" % model.__name__)

class Stack(models.Model):
    name              = models.CharField(max_length=80)
    numvms            = models.IntegerField(default=0)
    vms               = models.ManyToManyField(VM,blank=True,null=True,related_name='vms')
    status            = models.CharField(max_length=20, default='N/A')
    createdby         = models.ForeignKey(User,default=1,blank=True)
    createdwhen       = models.DateTimeField(editable=True,blank=True,null=True)
    price             = models.IntegerField(blank=True,null=True)
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        #self.createdwhen = datetime.now()
        self.createdwhen = timezone.now()
        if self.name == '':
            self.name = self.createdwhen
        super(Stack, self).save(*args, **kwargs)
    def kill(self, *args, **kwargs):
        vms       = self.vms.values()
        results   = []
        for vm in vms:
            name = vm['name']
            vmid = vm['id']
            vm = VM.objects.get(id=vmid)
            vm.kill()
            vm.delete()
            results.append(name)
        return  results
    def show(self, *args, **kwargs):
        vms       = self.vms.values()
        results   = {}
        for vm in vms:
            vmid = vm['id']
            name = vm['name']
            results[name] = "%s/vms/console/?id=%s" % ( baseurl, vmid)
        return  results
    def start(self, *args, **kwargs):
        vms       = self.vms.values()
        results   = {}
        for vm in vms:
            name = vm['name']
            vmid = vm['id']
            results[name] = "%s/vms/console/?id=%s" % ( baseurl, vmid)
            vm = VM.objects.get(id=vmid)
            vm.start()
        return  results
    def stop(self, *args, **kwargs):
        vms       = self.vms.values()
        results   = []
        for vm in vms:
            name = vm['name']
            vmid = vm['id']
            vm = VM.objects.get(id=vmid)
            vm.stop()
            results.append(name)
        return  results
