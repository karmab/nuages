# Views here.
import ast
import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from portal.models import VM,Profile,PhysicalProvider,VirtualProvider,CobblerProvider,ForemanProvider,IpamProvider,Type,Storage,Default,Partitioning
import time
from portal.ovirt import Ovirt
from portal.cobbler import Cobbler
from portal.foreman import Foreman
import django.utils.simplejson as json
from portal.forms import VMForm,StorageForm,OracleForm,ApacheForm,RacForm,SapForm,WeblogicForm,PartitioningForm
import time,datetime
from random import choice
import json
from django.contrib.auth.decorators import login_required
from portal.models import Apache, Oracle, Rac
from django.contrib.auth.models import User,Group
import logging
import random
from portal.ilo import Ilo
from portal.auth import LdapBackend
import socket
from django.db.models import Q

def checkconn(host,port):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)
		sock.connect((host, port))
		return True
	except socket.error:
		return False


def checkstorage(numvms,virtualprovider,disksize1,disksize2,storagedomain):
	size = int(disksize1)
	if disksize2:
		size = size+float(disksize2)
	size = numvms*size
	if virtualprovider.type =='ovirt':
		ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
		storageinfo = ovirt.getstorage()
		ovirt.close()
		remaining = int(storageinfo[storagedomain][1]) - size
		if remaining <=0:
			return "Not enough space on storagedomain %s.%s GB needed !"  % (storagedomain,size)
		else:
			return 'OK'
	elif virtualprovider.type == 'vsphere':
		jythoncommand = "/usr/bin/jython /portal/vsphere.py/%s %s %s %s %s %s %s" % (os.environ['PWD'], 'getstorage', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu )
		storageinfo = os.popen(jythoncommand).read()
		storageinfo= ast.literal_eval(storageinfo)	
		remaining = int(storageinfo[storagedomain][1]) - size
		if remaining <=0:
			return "Not enough space on storagedomain %s.%s GB needed !"  % (storagedomain,size)
		else:
			return 'OK'


@login_required
def create(request):
	username	  = request.user.username
	username	  = User.objects.filter(username=username)[0]
	logging.debug("prout")
	if request.method == 'POST':
		numvms  	  = request.POST.get('numvms')
		name   		  = request.POST.get('name')
                storagedomain     = request.POST.get('storagedomain')
		physicalprovider  = request.POST.get('physicalprovider')
		virtualprovider   = request.POST.get('virtualprovider')
		physical          = request.POST.get('physical')
		cobblerprovider   = request.POST.get('cobblerprovider')
		foremanprovider   = request.POST.get('foremanprovider')
                profile           = request.POST.get('profile')
                ip1               = request.POST.get('ip1')
                mac1              = request.POST.get('mac1')
                ip2               = request.POST.get('ip2')
                mac2              = request.POST.get('mac2')
                ip3               = request.POST.get('ip3')
                mac3              = request.POST.get('mac3')
                ip4               = request.POST.get('ip4')
                mac4              = request.POST.get('mac4')
                iso               = request.POST.get('iso')
                type              = request.POST.get('type')
                puppetclasses     = request.POST.get('puppetclasses')
                puppetparameters  = request.POST.get('puppetparameters')
                cobblerparameters = request.POST.get('cobblerparameters')
                ipilo             = request.POST.get('ipilo')
                numvms            = int(request.POST.get('numvms'))
                hostgroup         = request.POST.get('hostgroup')
		username	  = request.user.username
		username	  = User.objects.filter(username=username)[0]
		if physical == 'false':
			physical = False
		else:
			physical= True
		#get associated profiles
		#TODO:add tags to model
		tags=None
		profile=Profile.objects.filter(id=profile)[0]
		if storagedomain == '' and not physical:
			return HttpResponse("<font color='red'>Storage Domain is needed<p></font>")
		clu,guestid,memory,numcpu,disksize1,diskformat1,disksize2,diskformat2,diskinterface,numinterfaces,net1,subnet1,net2,subnet2,net3,subnet3,net4,subnet4,netinterface,dns,foreman,cobbler,requireip=profile.clu,profile.guestid,profile.memory,profile.numcpu,profile.disksize1,profile.diskformat1,profile.disksize2,profile.diskformat2,profile.diskinterface,profile.numinterfaces,profile.net1,profile.subnet1,profile.net2,profile.subnet2,profile.net3,profile.subnet3,profile.net4,profile.subnet4,profile.netinterface,profile.dns,profile.foreman,profile.cobbler,profile.requireip
		ipamprovider = profile.ipamprovider
		if requireip and not ipamprovider and not ip1:
			return HttpResponse("<font color='red'>Ip1 needed <p></font>")
		if requireip and not ipamprovider and not numinterfaces > 1 and not ip2:
			return HttpResponse("<font color='red'>Ip2 needed <p></font>")
		if requireip and not ipamprovider and numinterfaces > 2 and not ip3:
			return HttpResponse("<font color='red'>Ip3 needed <p></font>")
		if requireip and not ipamprovider and numinterfaces > 3 and not ip4:
			return HttpResponse("<font color='red'>Ip4 needed <p></font>")
		if profile.partitioning:	
			partitioninglist = cobblerparameters.split(' ')
			totalsize=0
			for element in partitioninglist:
				element=element.split('=')
				if element[0].endswith('size'):
					totalsize = totalsize+int(element[1])
			if int(disksize1)*1024 < totalsize:
				return HttpResponse("<font color='red'>Not enough space in disk1 according to your partitioning scheme. %d Mb needed <p></font>" % totalsize)
		if physical:
			physicalprovider = PhysicalProvider.objects.filter(id=physicalprovider)[0]
			virtualprovider = None
		else:
			virtualprovider = VirtualProvider.objects.filter(id=virtualprovider)[0]
			physicalprovider = None
		if cobbler and request.POST.get('cobblerprovider') != '':
			cobblerprovider=CobblerProvider.objects.filter(id=cobblerprovider)[0]
		else:
			cobblerprovider=None
		if foreman and request.POST.get('foremanprovider') != '':
			foremanprovider=ForemanProvider.objects.filter(id=foremanprovider)[0]
		else:
			foremanprovider=None
		if type:
			type2=Type.objects.filter(id=type)[0]
			cobblerparameters = "type=%s %s" % (type2.name, cobblerparameters)
		else:
			type2=None
		
		#CHECK SECTION
		if not physical and virtualprovider.type =='vsphere' and disksize2:
			return HttpResponse("Multiple disks arent supported at the moment for vsphere...")
		#MAKE SURE VM DOESNT ALLREADY EXISTS IN DB
		vms = VM.objects.filter(name=name)
		if len(vms) > 0:
			return HttpResponse("<font color='red'>VM %s allready exists<p></font>" % name)
		if not physical:
			storageresult=checkstorage(numvms,virtualprovider,disksize1,disksize2,storagedomain)
			if storageresult != 'OK':
				return HttpResponse("<font color='red'>%s<p></font>" % storageresult)
		#VM CREATION IN DB
		newvm=VM(name=name,storagedomain=storagedomain,physicalprovider=physicalprovider,virtualprovider=virtualprovider,physical=physical,cobblerprovider=cobblerprovider,foremanprovider=foremanprovider,profile=profile,ip1=ip1,mac1=mac1,ip2=ip2,mac2=mac2,ip3=ip3,mac3=mac3,ip4=ip4,mac4=mac4,type=type2,puppetclasses=puppetclasses,puppetparameters=puppetparameters, cobblerparameters=cobblerparameters,createdby=username,iso=iso,ipilo=ipilo,hostgroup=hostgroup)
		success = newvm.save()
		if success != 'OK':
				return HttpResponse("<font color='red'>%s<p></font>" % success)
		if numvms > 1:
			successes={ name : "Machine %s successfully created!!!" % name }
			for num in range(2,numvms+1):
				newname=request.POST.get("name_%s" % num)
				newip1=request.POST.get("ip1_%s" % num)
				newmac1=request.POST.get("mac1_%s" % num)
				newip2=request.POST.get("ip2_%s" % num)
				newip3=request.POST.get("ip3_%s" % num)
				newip4=request.POST.get("ip4_%s" % num)
				if requireip and not ipamprovider and not newip1:
					successes[newname]="<font color='red'>Ip1 needed for %s<p></font>" % newname
					continue
				if requireip and not ipamprovider and not numinterfaces > 1 and not newip2:
					successes[newname]="<font color='red'>Ip2 needed for %s<p></font>" % newname
					continue
				if requireip and not ipamprovider and numinterfaces > 2 and not newip3:
					successes[newname]="<font color='red'>Ip3 needed for %s<p></font>" % newname
					continue
				if requireip and not ipamprovider and numinterfaces > 3 and not newip4:
					successes[newname]="<font color='red'>Ip4 needed for %s<p></font>" % newname
					continue
				newvm=VM(name=newname,storagedomain=storagedomain,physicalprovider=physicalprovider,virtualprovider=virtualprovider,physical=physical,cobblerprovider=cobblerprovider,foremanprovider=foremanprovider,profile=profile,ip1=newip1,mac1=newmac1,ip2=newip2,mac2=mac2,ip3=newip3,mac3=mac3,ip4=newip4,mac4=mac4,type=type2,puppetclasses=puppetclasses,puppetparameters=puppetparameters, cobblerparameters=cobblerparameters,createdby=username,iso=iso,ipilo=ipilo,hostgroup=hostgroup)
				success = newvm.save()
				if success == 'OK':
					successes[newname]="Machine %s successfully created!!!" % newname
				else:
					successes[newname]=success
		if request.is_ajax():
			if numvms ==1:
				return HttpResponse("Machine %s successfully created!!!" % name)
			else:
				return HttpResponse( " ".join(successes.values()))
				
		else:
			return render(request, 'create.html', { 'created': True,'name': name, 'username': username } )
	else:
		apacheform       = ApacheForm()
		oracleform       = OracleForm()
		racform          = RacForm()
		sapform          = SapForm()
		weblogicform     = WeblogicForm()
		partitioningform = PartitioningForm()
		vmform = VMForm()
		return render(request, 'create.html', { 'vmform': vmform, 'username': username , 'apacheform': apacheform, 'oracleform': oracleform , 'racform' : racform, 'sapform' : sapform , 'weblogicform' : weblogicform , 'partitioningform' : partitioningform } )


@login_required
def profiles(request):
	logging.debug("prout")
	username	  = request.user.username
	username	  = User.objects.filter(username=username)[0]
	groups		  = username.groups
	profiles=Profile.objects.all()
        if request.method == 'POST' and request.is_ajax():
            profile = request.POST['profile']
	    profile=Profile.objects.filter(name=profile)[0]
	    cobblerprofile=profile.name
	    providers = ""
	    if profile.cobblerprofile:
	    	cobblerprofile=profile.cobblerprofile
            return HttpResponse("Cobbler: %s<p>Datacenter: %s<p>Cluster: %s<p>Numcpu: %s<p>Memory: %s<p>Guestid: %s<p>Disksize1 in Gb: %s<p>Numero Interfaces: %s<p>Foreman Support: %s<p>Cobbler Support:%s<p>Iso: %s<p>Virtual Provider: %s<p>Physical Provider: %s<p>" % (cobblerprofile,profile.datacenter,profile.clu,profile.numcpu,profile.memory,profile.guestid,profile.disksize1,profile.numinterfaces,profile.foreman,profile.cobbler,profile.iso,profile.virtualprovider,profile.physicalprovider ))
        else:
#	    usergroups=[]
#	    for g in groups.values():
#		usergroups.append(g['name'])
#            profiles=[]
#	    allprofiles=Profile.objects.all()
#	    for p in allprofiles:
#		found = False
#		profilegroup=p.groups.values()
#		if len(profilegroup) == 0:
#			profiles.append(p)
#		else:
#			for g in profilegroup:
#				if g['name'] in usergroups:
#					profiles.append(p)
	    profiles=Profile.objects.all()
	    return render(request, 'profiles.html', { 'profiles': profiles, 'username': username } )

#@login_required
def storage(request):
	logging.debug("prout")
	username	  = request.user.username
	username	  = User.objects.filter(username=username)[0]
	if request.is_ajax() and request.method == 'POST':
		virtualprovider = request.POST.get('virtualprovider')
		virtualprovider = VirtualProvider.objects.filter(name=virtualprovider)[0]
		connection = checkconn(virtualprovider.host,virtualprovider.port)
		if not connection:
			errorinfo=[ { 'failure' : "Host %s cant be reached" % virtualprovider.host } ]
			errorinfo = json.dumps(errorinfo)
        		return HttpResponse(errorinfo,mimetype='application/json')
		if virtualprovider.type == 'ovirt':
 			ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			storageinfo = ovirt.getstorage()
			ovirt.close()
			#add storage domains to DB if they dont exist
			for stor in storageinfo.keys():
				if not Storage.objects.filter(name=stor).exists():
					datacenter = storageinfo[stor][2]
					storage=Storage(name=stor,type=virtualprovider.type,provider=virtualprovider,datacenter=datacenter)
				 	storage.save()
			storageinfo = json.dumps(storageinfo)
        		return HttpResponse(storageinfo,mimetype='application/json')
		elif virtualprovider.type == 'vsphere':
			jythoncommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (os.environ['PWD'], 'getstorage', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu )
			storageinfo = os.popen(jythoncommand).read()
			storageinfo= ast.literal_eval(storageinfo)	
			#add storage domains to DB if they dont exist
			for stor in storageinfo.keys():
				if not Storage.objects.filter(name=stor).exists():
					datacenter = storageinfo[stor][2]
					storage=Storage(name=stor,type=virtualprovider.type,provider=virtualprovider,datacenter=datacenter)
				 	storage.save()
			storageinfo = json.dumps(storageinfo)
       			return HttpResponse(storageinfo,mimetype='application/json')
        else:
		vproviders=VirtualProvider.objects.filter(Q(type='ovirt')|Q(type='vsphere'))
		form = StorageForm()
		return render(request, 'storage.html', { 'vproviders' : vproviders ,'username': username } )


@login_required
def type(request):
	if request.method == 'POST' or request.is_ajax():
		type= request.POST.get('type').capitalize()
		if type=="Default":
			attributes=[]
			return HttpResponse(attributes,mimetype='application/json')
		exec("type=%s()" % type)
		attributes=[]
		for attr in type.__dict__:
			if not attr in  ['_state','id']: attributes.append(attr)
		attributes = json.dumps(attributes)
		return HttpResponse(attributes,mimetype='application/json')


@login_required
def profileinfo(request):
	if request.method == 'POST' or request.is_ajax():
		physical = False
		profile = request.POST.get('profile')
	    	profile = Profile.objects.filter(id=profile)[0]
	    	datacenter = profile.datacenter
		specific=[]
		storages=[]
		vlist=[]
		if request.POST.has_key('physical') and request.POST.get('physical') == 'true':
			physical = True
			physicalprovider=profile.physicalprovider
			if not physicalprovider:
				physical=False
				type='noilo'
				provider = ''
			else:
				type=physicalprovider.type
				provider = "%s,%s" % (physicalprovider.id, physicalprovider.name)
		else:
			virtualprovider=profile.virtualprovider
			type=virtualprovider.type
			provider = "%s,%s" % (virtualprovider.id, virtualprovider.name)
			storagelist=Storage.objects.filter(provider=virtualprovider,datacenter=datacenter)
			for stor in storagelist: 
				storages.append(stor.name)
		if physical and request.POST.has_key('ipilo'):
			type = 'ilo'
			ipilo = request.POST.get('ipilo')
			ilo=Ilo(ipilo,physicalprovider.user,physicalprovider.password)
			macs = ilo.getmacs()
			for mac in macs:
				specific.append(mac)
		if type =='ovirt' and profile.iso:
				type = 'iso'
				specific=[]
 				ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
				isos = ovirt.getisos()
				ovirt.close()
				isoslist=[]
				for iso in isos: 
					specific.append(iso)
		results = [type,profile.hide ,provider,specific,profile.foreman, profile.cobbler,profile.partitioning,profile.numinterfaces,storages]
		if profile.cobbler:
			cobblerprovider=profile.cobblerprovider
			cobblerprovider = "%s,%s" % (cobblerprovider.id, cobblerprovider.name)
			results.append(cobblerprovider)
		else:
			results.append('')
		if profile.foreman:
			foremanprovider=profile.foremanprovider
			foremaninfo = "%s,%s" % (foremanprovider.id, foremanprovider.name)
			results.append(foremaninfo)
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(5)
				sock.connect((foremanprovider.host, foremanprovider.port))
				available = True
			except socket.error:
				available=False
			if available:
				foremanhost, foremanport, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port, foremanprovider.user, foremanprovider.password
				foreman= Foreman(host=foremanhost, user=foremanuser, password=foremanpassword)
				hostgroups= foreman.hostgroups()
				results.append(hostgroups)
			else:
				results.append([''])
		else:
			results.append('')
		
		results = json.dumps(results)
		return HttpResponse(results,mimetype='application/json')

@login_required
def virtualprovidertype(request):
	if request.method == 'POST' or request.is_ajax():
		virtualprovider = request.POST.get('virtualprovider')
	    	virtualprovider = VirtualProvider.objects.filter(id=virtualprovider)[0]
		results = [virtualprovider.type]
		if virtualprovider.type == 'ilo' and request.POST.has_key('ipilo'):
			ipilo = request.POST.get('ipilo')
			ilo=Ilo(ipilo,virtualprovider.user,virtualprovider.password)
			macs = ilo.getmacs()
			for mac in macs:
				results.append(mac)
		if virtualprovider.type == 'ovirt' and request.POST.has_key('profile'):
			profile = request.POST.get('profile')
			profile = Profile.objects.filter(id=profile)[0]
			if profile.iso:
 				ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
				isos = ovirt.getisos()
				ovirt.close()
				isoslist=[]
				results=['iso']
				for iso in isos: 
					results.append(iso)
		results = json.dumps(results)
		return HttpResponse(results,mimetype='application/json')

@login_required
def yourvms(request):
	username	  = request.user.username
	username	  = User.objects.filter(username=username)[0]
	vms = VM.objects.filter(createdby=username)
	default = Default.objects.all()[0]
	resultvms=[]
	removed=[]
	for vm in vms:
		name = vm.name
		#handle physical machines
		if vm.physical:
			ipilo=vm.ipilo
			physicalprovider=vm.physicalprovider
			try:
                		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                		sock.settimeout(5)
                		sock.connect((ipilo, 22))
				ipilo = vm.ipilo
				ilo=Ilo(ipilo,physicalprovider.user,physicalprovider.password)
				status = ilo.status()
				vm.status = status
				resultvms.append(vm)
				continue
        		except:
				continue
		virtualprovider = vm.virtualprovider
		try:
                	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                	sock.settimeout(5)
                	sock.connect((virtualprovider.host, virtualprovider.port))
        	except socket.error:
			continue
		if not vm.physical and virtualprovider.type == 'ovirt':
 			ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			status = ovirt.status(name)
			ovirt.close()
		if not vm.physical and virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			statuscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'status', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
			status = os.popen(statuscommand).read()
			if status =='': status = None
		if not status:
			vm.delete()	
			removed.append(vm)
		else:
			vm.status = status
			resultvms.append(vm)
	if len(removed) >= 1:
		return render(request, 'yourvms.html', { 'vms': resultvms , 'removed': removed, 'username': username , 'default' : default } )
	else:
		return render(request, 'yourvms.html', { 'vms': resultvms, 'username': username , 'default' : default } )


@login_required
def allvms(request):
	username	  = request.user.username
	username          = User.objects.filter(username=username)[0]
	if not username.is_staff:
		return render(request, 'restricted.html' )
	if request.method == 'POST' or request.is_ajax():
		resultvms=[]
		virtualprovidername = request.POST.get('virtualprovider')
	    	virtualprovider = VirtualProvider.objects.filter(name=virtualprovidername)[0]
		if virtualprovider.type == 'ovirt':
			ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			vms = ovirt.allvms()
			ovirt.close()
			for vm in vms:
				resultvms.append( {'name':vm, 'status':vms[vm],'virtualprovider':virtualprovidername } )
			return render(request, 'allvms2.html', { 'vms': resultvms , 'console' : True , 'username': username } )
		if virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			allvmscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s" % (os.environ['PWD'],'allvms', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu)
			results = os.popen(allvmscommand).read()
			vms= ast.literal_eval(results)	
			for vm in vms:
				resultvms.append( {'name':vm, 'status':vms[vm],'virtualprovider':virtualprovidername } )
			return render(request, 'allvms2.html', { 'vms': resultvms, 'username': username } )
	else:
		vproviders=VirtualProvider.objects.filter(Q(type='ovirt')|Q(type='vsphere'))
		form = StorageForm()
		return render(request, 'allvms.html', { 'vproviders' : vproviders , 'username': username} )


@login_required
def console(request):
	username	  = request.user.username
	username	  = User.objects.filter(username=username)[0]
	if request.method == 'GET'and request.GET.has_key('vm'):
		vmname = request.GET.get('vm')
		if request.GET.has_key('virtualprovider'):
			virtualprovidername=request.GET.get('virtualprovider')
		else:
			vm = VM.objects.filter(name=vmname)[0]
			virtualprovidername = vm.virtualprovider
	    	virtualprovider = VirtualProvider.objects.filter(name=virtualprovidername)[0]
		default = Default.objects.all()[0]
                if virtualprovider.type == 'ovirt':
                        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			host,port,ticket,protocol = ovirt.console(vmname)
			ovirt.close()
			sockhost=default.consoleip
			sockport = random.randint(10000,60000)
			pwd = os.environ["PWD"]
			information = { 'host' : sockhost , 'port' : sockport , 'ticket' : ticket }
			vm = {'name': vmname , 'virtualprovider' : virtualprovider , 'status' : 'up' }
			if protocol =="spice":
				pwd = os.environ["PWD"]
				cert="%s/%s.pem" % (pwd,virtualprovider.name)
				websockifycommand = "websockify %s -D --timeout=30 --cert %s --ssl-target %s:%s" % (sockport,cert,host,port)
				os.popen(websockifycommand)
				return render(request, 'spice.html', { 'information' : information ,  'vm' : vm , 'username': username } )
			elif protocol =="vnc":
				websockifycommand = "websockify %s -D --timeout=30 %s:%s" % (sockport,host,port)
				os.popen(websockifycommand)
				return render(request, 'vnc.html', { 'information' : information ,  'vm' : vm , 'username': username } )
		else:
			return HttpResponse("Console not only implemented for %s" % virtualprovider.type )
	else:
			return redirect('portal.views.yourvms')
		

@login_required
def start(request):
	if request.method == 'POST':
		vmname = request.POST.get('name')
		virtualprovider=request.POST.get('virtualprovider')
	    	virtualprovider = VirtualProvider.objects.filter(name=virtualprovider)[0]
                if virtualprovider.type == 'ovirt':
                        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			results=ovirt.start(vmname)
			ovirt.close()
			return HttpResponse(results)
		elif virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			startcommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'start', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,vmname )
			start = os.popen(startcommand).read()
			startinfo= ast.literal_eval(start)	
			startinfo = json.dumps(startinfo)
       			return HttpResponse(startinfo,mimetype='application/json')

@login_required
def stop(request):
	if request.method == 'POST':
		vmname = request.POST.get('name')
		virtualprovider=request.POST.get('virtualprovider')
	    	virtualprovider = VirtualProvider.objects.filter(name=virtualprovider)[0]
                if virtualprovider.type == 'ovirt':
                        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			results= ovirt.stop(vmname)
			ovirt.close()
			return HttpResponse(results)
		elif virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			stopcommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'stop', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,vmname )
			stop = os.popen(stopcommand).read()
			stopinfo= ast.literal_eval(stop)	
			stopinfo = json.dumps(stopinfo)
       			return HttpResponse(stopinfo,mimetype='application/json')

@login_required
def kill(request):
	if request.method == 'POST':
		name = request.POST.get('name')
	    	vm = VM.objects.filter(name=name)[0]
		virtualprovider=vm.virtualprovider
		cobblerprovider=vm.cobblerprovider
		foremanprovider=vm.foremanprovider
		results=[]
		if cobblerprovider:
                        cobblerhost, cobbleruser, cobblerpassword = cobblerprovider.host, cobblerprovider.user, cobblerprovider.password
                        cobbler=Cobbler(cobblerhost, cobbleruser, cobblerpassword)
			r=cobbler.remove(name)
		if foremanprovider:
			dns = vm.profile.dns
                        foremanhost, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.user, foremanprovider.password
                        foreman=Foreman(host=foremanhost, user=foremanuser, password=foremanpassword)
			r=foreman.delete(name=name,dns=dns)
                if virtualprovider and virtualprovider.type == 'ovirt':
                        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			r=ovirt.remove(name)
			ovirt.close()
		elif virtualprovider and virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			removecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'remove', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
			remove = os.popen(removecommand).read()
			removeinfo= ast.literal_eval(remove)	
			r='VM killed in vsphere'
			#removeinfo = json.dumps(removeinfo)
       			#return HttpResponse(removeinfo,mimetype='application/json')
		vm.delete()
		return HttpResponse("VM %s killed" % name)

@login_required
def hostgroups(request):
	if request.method == 'POST':
		foremanprovider=request.POST.get('foremanprovider')
	    	foremanprovider = ForemanProvider.objects.filter(id=foremanprovider)[0]
		foremanhost, foremanport, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port, foremanprovider.user, foremanprovider.password
		foreman= Foreman(host=foremanhost, user=foremanuser, password=foremanpassword)
		hostgroups= foreman.hostgroups()
		hostgroups = json.dumps(hostgroups)
       		return HttpResponse(hostgroups,mimetype='application/json')
