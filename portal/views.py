# Views here.
import ast
import fileinput
import os
from django.http import HttpResponse
from django.shortcuts import render,redirect
from portal.models import *
from portal.ovirt import Ovirt
from portal.kvirt import Kvirt
from portal.cobbler import Cobbler
from portal.foreman import Foreman
import django.utils.simplejson as json
from portal.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import logging
import random
from portal.ilo import Ilo
from portal.oa import Oa
import socket
from django.db.models import Q
from datetime import datetime
from calendar import monthrange

if os.path.exists("portal/customtypes.py"):
	from customtypes import *


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
	if virtualprovider.type =='kvirt':
		kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
		storageinfo = kvirt.getstorage()
		kvirt.close()
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
                parameters        = request.POST.get('parameters')
                ipilo             = request.POST.get('ipilo')
                numvms            = int(request.POST.get('numvms'))
                hostgroup         = request.POST.get('hostgroup')
		if physical == 'false':
			physical = False
		else:
			physical= True
		#get associated profiles
		#TODO:add tags to model
		tags=None
		profile=Profile.objects.filter(id=profile)[0]
		if storagedomain == '' and not physical:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Storage Domain is needed<p</div>") 
		clu,guestid,memory,numcpu,disksize1,diskformat1,disksize2,diskformat2,diskinterface,numinterfaces,net1,subnet1,net2,subnet2,net3,subnet3,net4,subnet4,netinterface,dns,foreman,cobbler,requireip=profile.clu,profile.guestid,profile.memory,profile.numcpu,profile.disksize1,profile.diskformat1,profile.disksize2,profile.diskformat2,profile.diskinterface,profile.numinterfaces,profile.net1,profile.subnet1,profile.net2,profile.subnet2,profile.net3,profile.subnet3,profile.net4,profile.subnet4,profile.netinterface,profile.dns,profile.foreman,profile.cobbler,profile.requireip
		ipamprovider = profile.ipamprovider
		if requireip and not ipamprovider and not ip1:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Ip1 needed <p><p</div>")
		if requireip and not ipamprovider and not numinterfaces > 1 and not ip2:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Ip2 needed <p><p</div>")
		if requireip and not ipamprovider and numinterfaces > 2 and not ip3:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Ip3 needed <p><p</div>")
		if requireip and not ipamprovider and numinterfaces > 3 and not ip4:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Ip4 needed <p><p</div>")
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
			parameters = "type=%s %s" % (type, parameters)
		
		#CHECK SECTION
		if not physical and virtualprovider.type =='vsphere' and disksize2:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Multiple disks arent supported at the moment for vsphere...<p><p</div>")
		#MAKE SURE VM DOESNT ALLREADY EXISTS IN DB WITH THIS SAME VIRTUALPROVIDER
		vms = VM.objects.filter(name=name).filter(virtualprovider=virtualprovider)
		if len(vms) > 0:
			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>VM %s allready exists</div>" % name)
		if not physical and not virtualprovider.type == 'fake' and not profile.autostorage:
			storageresult=checkstorage(numvms,virtualprovider,disksize1,disksize2,storagedomain)
			if storageresult != 'OK':
				return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>%s</div>" % storageresult )
		#VM CREATION IN DB
		newvm=VM(name=name,storagedomain=storagedomain,physicalprovider=physicalprovider,virtualprovider=virtualprovider,physical=physical,cobblerprovider=cobblerprovider,foremanprovider=foremanprovider,profile=profile,ip1=ip1,mac1=mac1,ip2=ip2,mac2=mac2,ip3=ip3,mac3=mac3,ip4=ip4,mac4=mac4,puppetclasses=puppetclasses,parameters=parameters,createdby=username,iso=iso,ipilo=ipilo,hostgroup=hostgroup)
		success = newvm.save()
		if success != 'OK':
				return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>%s</div>" % success )
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
					successes[newname]="Ip1 needed for %s" % newname
					continue
				if requireip and not ipamprovider and not numinterfaces > 1 and not newip2:
					successes[newname]="Ip2 needed for %s" % newname
					continue
				if requireip and not ipamprovider and numinterfaces > 2 and not newip3:
					successes[newname]="Ip3 needed for %s" % newname
					continue
				if requireip and not ipamprovider and numinterfaces > 3 and not newip4:
					successes[newname]="Ip4 needed for %s" % newname
					continue
				newvm=VM(name=newname,storagedomain=storagedomain,physicalprovider=physicalprovider,virtualprovider=virtualprovider,physical=physical,cobblerprovider=cobblerprovider,foremanprovider=foremanprovider,profile=profile,ip1=newip1,mac1=newmac1,ip2=newip2,mac2=mac2,ip3=newip3,mac3=mac3,ip4=newip4,mac4=mac4,puppetclasses=puppetclasses,parameters=parameters,createdby=username,iso=iso,ipilo=ipilo,hostgroup=hostgroup)
				success = newvm.save()
				if success == 'OK':
					successes[newname]="Machine %s successfully created!!!" % newname
				else:
					successes[newname]=success
		if request.is_ajax():
			if numvms ==1:
				return HttpResponse("<div class='alert alert-success' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Machine %s successfully created!!!</div>" % name )
			else:
				return HttpResponse("<div class='alert alert-info' ><button type='button' class='close' data-dismiss='alert'>&times;</button>%s</div>" % " ".join(successes.values()) )
				
		else:
			return render(request, 'create.html', { 'created': True,'name': name, 'username': username } )
	else:
		vmform =  VMForm(request.user)
		customforms=[]
		if os.path.exists("portal/customtypes.py"):
			import customtypes
			for element in dir(customtypes):
				if not element.startswith("__") and element != "forms":
					exec("customform=%s()" % element)
					customforms.append({'name':element,'form':customform})
			return render(request, 'create.html', { 'vmform': vmform, 'username': username , 'customforms' : customforms } )
		else:
			return render(request, 'create.html', { 'vmform': vmform, 'username': username } )

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
            return HttpResponse("<div class='alert alert-success' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Cobbler Profile: %s<p><p>Datacenter: %s<p>Cluster: %s<p>Number of cpus: %s<p>Memory: %sMo<p>Guestid: %s<p>Disksize first disk : %sGb<p>Number of network interfaces: %s<p>Foreman Enabled: %s<p>Cobbler Enabled:%s<p>Isos List Enabled: %s<p>Virtual Provider: %s<p>Physical Provider: %s<p></div>" % (cobblerprofile,profile.datacenter,profile.clu,profile.numcpu,profile.memory,profile.guestid,profile.disksize1,profile.numinterfaces,profile.foreman,profile.cobbler,profile.iso,profile.virtualprovider,profile.physicalprovider ))
        elif username.is_staff:
	    profiles = Profile.objects.all()
	    if not profiles:
        	information = { 'title':'Missing elements' , 'details':'Create profiles first...' }
        	return render(request, 'information.html', { 'information' : information } )
	    else:
	    	return render(request, 'profiles.html', { 'profiles': profiles , 'username': username } )
	else:
	    usergroups=[]
	    for g in groups.values():
		usergroups.append(g['id'])
	    if len(usergroups) == 0:
	    	query = Q(groups=None)
	    else:
	    	query = Q(groups=None)|Q(groups=usergroups[0])
	    	for group in usergroups[1:]:
			query=query|Q(groups=group)
	    query=Profile.objects.filter(query)
            if not query:
        	information = { 'title':'Missing elements' , 'details':'Create profiles first...' }
        	return render(request, 'information.html', { 'information' : information } )
            else:
	        return render(request, 'profiles.html', { 'profiles': query , 'username': username } )

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
		elif virtualprovider.type == 'kvirt':
			kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
			storageinfo = kvirt.getstorage()
			kvirt.close()
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
		if username.is_staff:
			vproviders=VirtualProvider.objects.filter(Q(type='ovirt')|Q(type='vsphere')|Q(type='kvirt'))
		else:
			usergroups = []
			groups		  = username.groups
	    		for g in groups.values():
				usergroups.append(g['id'])
	    		if len(usergroups) == 0:
	    			query = Q(groups=None)
	    		else:
	    			query = Q(groups=None)|Q(groups=usergroups[0])
	    			for group in usergroups[1:]:
					query = query|Q(groups=group)
	    		query = Profile.objects.filter(query)
            		if not query:
        			information = { 'title':'Missing elements' , 'details':'Create Profiles first...' }
        			return render(request, 'information.html', { 'information' : information } )
			vproviderslist = []
			for profile in query:
				if profile.virtualprovider and profile.virtualprovider.name not in vproviderslist:
					vproviderslist.append(profile.virtualprovider.name)
			vquery = Q(name=vproviderslist[0])
			for provider in vproviderslist:
				vquery = vquery|Q(name=provider)
			vproviders=VirtualProvider.objects.filter(Q(type='ovirt')|Q(type='vsphere')|Q(type='kvirt'))
			vproviders=vproviders.filter(vquery)
            	if not vproviders:
        		information = { 'title':'Missing elements' , 'details':'Create Virtual providers first...' }
        		return render(request, 'information.html', { 'information' : information } )
		else:
			form = StorageForm()
			return render(request, 'storage.html', { 'vproviders' : vproviders ,'username': username } )


@login_required
def types(request):
	if request.method == 'POST' or request.is_ajax():
		results=[[]]
		types= request.POST.get('types').split(',')
		otherclasses=[]
		import customtypes
                for element in dir(customtypes):
			if element in types:
                                exec("type=%s()" % element)
				for attr in type.fields.keys():
					results.append(attr)
                        elif not element.startswith('__') and element != "forms":
				otherclasses.append(element)
		results[0] = otherclasses
		results = json.dumps(results)
		return HttpResponse(results,mimetype='application/json')

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
			if type != "fake":
				provider = "%s,%s" % (virtualprovider.id, virtualprovider.name)
				storagelist=Storage.objects.filter(provider=virtualprovider,datacenter=datacenter)
				if profile.autostorage:	
					#RETRIEVE BEST STORAGE DOMAIN
					if type == 'ovirt':
 						ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
						storages = [ovirt.beststorage()]
						ovirt.close()
					elif type == 'kvirt':
						kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
						storages = [kvirt.beststorage()]
						kvirt.close()
					elif type == 'vsphere': 
						pwd = os.environ["PWD"]
                        			beststoragecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'beststorage', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
                        			bestds = os.popen(beststoragecommand).read()
						storages=[bestds]
					else:
						storages=["N/A"]
				else:
					for stor in storagelist: 
						storages.append(stor.name)
			else:
				provider = "%s,%s" % (virtualprovider.id, virtualprovider.name)
				storages=['N/A']
		if physical and request.POST.has_key('ipilo'):
			if physicalprovider.type=='ilo':
				type = 'ilo'
				ipilo = request.POST.get('ipilo')
				ilo=Ilo(ipilo,physicalprovider.user,physicalprovider.password)
				macs = ilo.getmacs()
				for mac in macs:
					specific.append(mac)
			elif physicalprovider.type=='oa' and request.POST.has_key('name'):
				name = request.POST.get('name')
				type = 'oa'
				ipilo = request.POST.get('ipilo')
				oa=Oa(ipilo,physicalprovider.user,physicalprovider.password)
				bladeid = oa.getid(name)
				macs = oa.getmacs(bladeid)
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
		if type =='kvirt' and profile.iso:
				type = 'iso'
				specific=[]
				kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
				isos = kvirt.getisos()
				kvirt.close()
				isoslist=[]
				for iso in isos: 
					specific.append(iso)
		results = [type,profile.hide ,provider,specific,profile.foreman, profile.cobbler,profile.numinterfaces,storages]
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
				foremanhost, foremanport, foremanuser, foremanpassword, foremanenv = foremanprovider.host, foremanprovider.port, foremanprovider.user, foremanprovider.password , foremanprovider.envid
				foreman= Foreman(host=foremanhost, port=foremanport,user=foremanuser, password=foremanpassword)
				hostgroups = foreman.hostgroups(foremanenv)
				results.append(hostgroups)
				classes = foreman.classes(foremanenv)
				results.append(classes)
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
		if virtualprovider.type == 'oa' and request.POST.has_key('ipilo') and request.POST.has_key('name'):
			name = request.POST.get('name')
			ipilo = request.POST.get('ipilo')
			oa=Oa(ipilo,virtualprovider.user,virtualprovider.password)
			bladeid = oa.getid(name)
			macs = oa.getmacs(bladeid)
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
		if virtualprovider.type == 'kvirt' and request.POST.has_key('profile'):
			profile = request.POST.get('profile')
			profile = Profile.objects.filter(id=profile)[0]
			if profile.iso:
				kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
				isos = kvirt.getisos()
				kvirt.close()
				isoslist=[]
				results=['iso']
				for iso in isos: 
					results.append(iso)
		results = json.dumps(results)
		return HttpResponse(results,mimetype='application/json')

@login_required
def yourvms(request):
	username	  = request.user.username
	username	  = User.objects.get(username=username)
	usergroups        = username.groups
	query		  = Q(createdby=username)
	allusers	  = User.objects.all()
	for g in usergroups.all():
		for u in allusers:
			if u.username == username.username:
				continue
			if g in u.groups.all():
				query=query|Q(createdby=u)
	vms = VM.objects.filter(query)		
	defaults = Default.objects.all()
	if not defaults:
		ip = socket.gethostbyname(socket.gethostname())
		default = Default(name='default',consoleip=ip)
		default.save()
	else:
		default = Default.objects.all()[0]
	resultvms=[]
	removed=[]
	activeproviders={}
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
				if physicalprovider.type =='ilo':
					ilo=Ilo(ipilo,physicalprovider.user,physicalprovider.password)
					status = ilo.status()
				elif physicalprovider.type =='oa':
					oa=Oa(ipilo,physicalprovider.user,physicalprovider.password)
					bladeid =oa.getid(name)
					status = oa.status(bladeid)
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
			#IMPROVE THIS CODE AS IT MAKES LOADING OF THE PAGE SLOW!!!
 			ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			status = ovirt.status(name)
			ovirt.close()
		if not vm.physical and virtualprovider.type == 'kvirt':
			kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
			status = kvirt.status(name)
			kvirt.close()
		if not vm.physical and virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			statuscommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'status', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
			status = os.popen(statuscommand).read()
			if status =='': status = None
		if not vm.physical and virtualprovider.type == 'fake':
			status = "N/A"
		if not status:
			vm.delete()	
			removed.append(vm)
		else:
			vm.status = status
			resultvms.append(vm)
	if len(removed) >= 1:
		return render(request, 'yourvms.html', { 'vms': resultvms , 'removed': removed, 'username': username , 'default' : default  } )
	else:
		return render(request, 'yourvms.html', { 'vms': resultvms, 'username': username , 'default' : default  } )


@login_required
def allvms(request):
	username	  = request.user.username
	username          = User.objects.filter(username=username)[0]
	if not username.is_staff:
		information = { 'title':'Nuages Restricted Information' , 'details':'Restricted access,sorry....' }
		return render(request, 'information.html', { 'information' : information } )
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
		if virtualprovider.type == 'kvirt':
			kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
			vms = kvirt.allvms()
			kvirt.close()
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
		vproviders=VirtualProvider.objects.filter(Q(type='ovirt')|Q(type='vsphere')|Q(type='kvirt'))
		form = StorageForm()
		return render(request, 'allvms.html', { 'vproviders' : vproviders , 'username': username} )


@login_required
def console(request):
	username	  = request.user.username
	username	  = User.objects.get(username=username)
	usergroups        = username.groups
	if request.method == 'GET':
		if request.GET.has_key('id'):
			vmid = request.GET.get('id')
			vm = VM.objects.get(id=vmid)
			vmname = vm.name
			virtualprovidername = vm.virtualprovider
			vmcreatedby = vm.createdby.username
            		if vmcreatedby !=username.username:
			    vmgroups = vm.createdby.groups
			    commongroup = False
			    for group in vmgroups.all():
				    if group in usergroups.all():
					    commongroup = True
					    break
			    if not commongroup:
				#return redirect('portal.views.yourvms')
				information = { 'title':'Console not authorized' , 'details':'Your user is not authorized to access this VM' }
				return render(request, 'information.html', { 'information' : information } )
		if request.GET.has_key('name') and request.GET.has_key('virtualprovider') and username.is_staff:
			vmname = request.GET.get('name')
			virtualprovidername = request.GET.get('virtualprovider')
	    	virtualprovider = VirtualProvider.objects.get(name=virtualprovidername)
		default = Default.objects.all()[0]
                if virtualprovider.type == 'ovirt' or virtualprovider.type == 'kvirt' :
			if virtualprovider.type == 'ovirt':
                        	ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
				host,port,ticket,protocol = ovirt.console(vmname)
				ovirt.close()
			if virtualprovider.type == 'kvirt':
				kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
				host,port,ticket,protocol = kvirt.console(vmname)
				kvirt.close()
				if not host:
					information = { 'title':'Console not configured' , 'details':'the display of this vm doesnt listen on the host ip' }
                			return render(request, 'information.html', { 'information' : information } )
			sockhost=default.consoleip
			sockport = random.randint(10000,60000)
			pwd = os.environ["PWD"]
			information = { 'host' : sockhost , 'port' : sockport , 'ticket' : ticket }
			vm = {'name': vmname , 'virtualprovider' : virtualprovider , 'status' : 'up' }
			if protocol =="spice" and virtualprovider.type == 'ovirt':
				pwd = os.environ["PWD"]
				cert="%s/%s.pem" % (pwd,virtualprovider.name)
				websockifycommand = "websockify %s -D --timeout=30 --cert %s --ssl-target %s:%s" % (sockport,cert,host,port)
				os.popen(websockifycommand)
				return render(request, 'spice.html', { 'information' : information ,  'vm' : vm , 'username': username } )
			if protocol =="spice" and virtualprovider.type == 'kvirt':
				pwd = os.environ["PWD"]
				#cert="%s/%s.pem" % (pwd,virtualprovider.name)
				#websockifycommand = "websockify %s -D --timeout=30 --cert %s --ssl-target %s:%s" % (sockport,cert,host,port)
				websockifycommand = "websockify %s -D --timeout=30 %s:%s" % (sockport,host,port)
				os.popen(websockifycommand)
				return render(request, 'spice.html', { 'information' : information ,  'vm' : vm , 'username': username } )
			elif protocol =="vnc":
				websockifycommand = "websockify %s -D --timeout=30 %s:%s" % (sockport,host,port)
				os.popen(websockifycommand)
				return render(request, 'vnc.html', { 'information' : information ,  'vm' : vm , 'username': username } )
		else:
			information = { 'title':'Console not implemented' , 'details':"Console not implemented for %s" % virtualprovider.type }
                	return render(request, 'information.html', { 'information' : information } )
	else:
			information = { 'title':'Wrong Console' , 'details':"something went wrong.Report to sysadmin" }
                	return render(request, 'information.html', { 'information' : information } )
		

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
                elif virtualprovider.type == 'kvirt':
			kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
			results=kvirt.start(vmname)
			kvirt.close()
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
	    	virtualprovider = VirtualProvider.objects.get(name=virtualprovider)
                if virtualprovider.type == 'ovirt':
                        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			results= ovirt.stop(vmname)
			ovirt.close()
			return HttpResponse(results)
                elif virtualprovider.type == 'kvirt':
			kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
			results= kvirt.stop(vmname)
			kvirt.close()
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
	logging.debug("prout")
	if request.method == 'POST':
		name     = request.POST.get('name')
		provider = request.POST.get('provider')
		if provider =='':
			virtualprovider = None
	    		vm = VM.objects.filter(name=name).filter(physical=True)[0]
		else:
			virtualprovider= VirtualProvider.objects.get(name=provider)
	    		vm = VM.objects.filter(name=name).filter(virtualprovider=virtualprovider)[0]
		cobblerprovider=vm.cobblerprovider
		foremanprovider=vm.foremanprovider
		results=[]
		if cobblerprovider:
                        cobblerhost, cobbleruser, cobblerpassword = cobblerprovider.host, cobblerprovider.user, cobblerprovider.password
                        cobbler=Cobbler(cobblerhost, cobbleruser, cobblerpassword)
			r=cobbler.remove(name)
		if foremanprovider:
			dns = vm.profile.dns
                        foremanhost, foremanport, foremanuser, foremanpassword = foremanprovider.host, foremanprovider.port,foremanprovider.user, foremanprovider.password
                        foreman=Foreman(host=foremanhost,port=foremanport,user=foremanuser, password=foremanpassword)
			r=foreman.delete(name=name,dns=dns)
                if virtualprovider and virtualprovider.type == 'ovirt':
                        ovirt = Ovirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,virtualprovider.password,virtualprovider.ssl)
			r=ovirt.remove(name)
			ovirt.close()
                elif virtualprovider and virtualprovider.type == 'kvirt':
			kvirt = Kvirt(virtualprovider.host,virtualprovider.port,virtualprovider.user,protocol='ssh')
			r=kvirt.remove(name)
			kvirt.close()
		elif virtualprovider and virtualprovider.type == 'vsphere':
			pwd = os.environ["PWD"]
			removecommand = "/usr/bin/jython %s/portal/vsphere.py %s %s %s %s %s %s %s" % (os.environ['PWD'],'remove', virtualprovider.host, virtualprovider.user, virtualprovider.password , virtualprovider.datacenter, virtualprovider.clu ,name )
			remove = os.popen(removecommand).read()
			removeinfo= ast.literal_eval(remove)	
			r='VM killed in vsphere'
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

@login_required
def customforms(request):
	logging.debug("prout")
	username	  = request.user.username
	username          = User.objects.filter(username=username)[0]
	if request.method == 'POST' and request.POST.has_key('type'):
		type= request.POST.get('type')
		attributes=[]
		exec("type=%s()" % type)
		for attr in type.fields:
			if 'max_length' in type.fields[attr].__dict__:
				fieldname='CharField'
				specific=type.fields[attr].initial
			elif '_choices' in type.fields[attr].__dict__:
				fieldname='ChoiceField'
				#specific=type.fields[attr].choices
				specific=[]
				for element in type.fields[attr].choices:
					specific.append(element[0])
			elif 'max_value' in type.fields[attr].__dict__:
				fieldname='IntegerField'
				specific=type.fields[attr].initial
			attributes.append([attr,fieldname,specific,type.fields[attr].required])
		attributes = json.dumps(attributes)
       		return HttpResponse(attributes,mimetype='application/json')
	else:
		if not os.path.exists("portal/customtypes.py"):
			information = { 'title':'No customforms' , 'details':'No customforms found.' }
                	return render(request, 'information.html', { 'information' : information } )
		types=[]
		import customtypes
                for element in dir(customtypes):
                        if not element.startswith('__') and element != "forms":
				types.append(element)
		return render(request, 'customforms.html', { 'username': username , 'types': types } )


@login_required
def customforminfo(request):
        logging.debug("prout")
        username          = request.user.username
        username          = User.objects.filter(username=username)[0]
        if request.method == 'POST':
                type= request.POST.get('type')
                exec("type=%s()" % type)
                return HttpResponse(type.as_table())
        else:
                types=[]
                import customtypes
                for element in dir(customtypes):
                        if not element.startswith('__') and element != "forms":
                                types.append(element)
                return render(request, 'customforms.html', { 'username': username , 'types': types } )

@login_required
def customformedit(request):
	logging.debug("prout")
	username	  = request.user.username
	username          = User.objects.filter(username=username)[0]
	if request.method == 'POST' and request.POST.has_key('type'):
		type= request.POST.get('type')
		attributes=[]
		exec("type=%s()" % type)
		for attr in type.fields:
			if 'max_length' in type.fields[attr].__dict__:
				fieldname='CharField'
				specific=type.fields[attr].initial
			elif '_choices' in type.fields[attr].__dict__:
				fieldname='ChoiceField'
				#specific=type.fields[attr].choices
				specific=[]
				for element in type.fields[attr].choices:
					specific.append(element[0])
			elif 'max_value' in type.fields[attr].__dict__:
				fieldname='IntegerField'
				specific=type.fields[attr].initial
			attributes.append([attr,fieldname,specific,type.fields[attr].required])
		attributes = json.dumps(attributes)
       		return HttpResponse(attributes,mimetype='application/json')
	else:
		if not os.path.exists("portal/customtypes.py"):
			#information = { 'title':'Missing customforms' , 'details':'Create customforms first!' }
                	#return render(request, 'information.html', { 'information' : information } )
                	return render(request, 'customformedit.html', { 'username': username  } )
		types=[]
		import customtypes
                for element in dir(customtypes):
                        if not element.startswith('__') and element != "forms":
				types.append(element)
		if request.is_ajax():
			types = json.dumps(types)
        		return HttpResponse(types,mimetype='application/json')
		else:
                	return render(request, 'customformedit.html', { 'username': username , 'types': types } )

@login_required
def customformupdate(request):
	logging.debug("prout")
	if request.method == 'POST' and request.POST.has_key('parameters') and request.POST.has_key('type'):
		type = request.POST['type'].capitalize()
		parameters = request.POST['parameters']
		if not os.path.exists("portal/customtypes.py") or not  open("portal/customtypes.py").readlines():
			f=open("portal/customtypes.py","a")
			f.write("from django import forms\n")
			f.close()
		if os.path.exists("portal/customtypes.py.lock"):
			response = "<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>customtypes  currently edited by another user</div>"
			return HttpResponse(response)
		else:
			#open lock file
			open("portal/customtypes.py.lock", 'a').close()
			types=[]
			import customtypes
                	for element in dir(customtypes):
                        	if not element.startswith('__') and element != "forms":
					types.append(element)
			#it s an existing type, we must first remove  along with all of its attribute
			if type in types:
				attributes=[]
				exec("form=%s()" % type)
				for attr in form.fields:
					attributes.append(attr)
				attributes.insert(0,type)
				#NOW WE NEED TO PARSE THE FILE AND REMOVE ACCORDINGLY LINES!!!!
				for line in fileinput.input("portal/customtypes.py", inplace=True):
					found = False
					for attribute in attributes:
						if attribute in line:
							found = True
							break
					if not found:
						print line,
			#now add it at the end of  customtypes.py
			#completefile = open("portal/customtypes.py").readlines()
			parameters = parameters.split(' ')
			#preliminary check for  uniqueness of parameters
			#for parameter in parameters:
			#	parameter=parameter.split(';')
			#	name=parameter[0]
			#	indices = [i for i, x in enumerate(completefile) if name in x ]
			#	if len(indices) >1:
			#		response = "<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>parameter names need to be unique</div>"
			#		return HttpResponse(response)
			f = open("portal/customtypes.py", 'a')
			f.write("class %s(forms.Form):\n" % type)
			for parameter in parameters:
				parameter=parameter.split(';')
				name=parameter[0]
				fieldtype=parameter[1]
				default=parameter[2]
				required=parameter[3]
				if fieldtype == "IntegerField" and default != '':
					f.write("\t%s\t= forms.%s(initial=%s)\n" % (name,fieldtype,int(default) ) )
				elif fieldtype == "CharField" and default != '':
					f.write("\t%s\t= forms.%s(initial=\"%s\")\n" % (name,fieldtype,default ) )
				elif fieldtype == "ChoiceField" and default != '':
					choices=''
					for choice in default.split(','):
						if choices == '':
							choices = "('%s', '%s')" % (choice,choice)
						else:	
							choices = choices+",('%s', '%s')" % (choice,choice)
					f.write("\t%s\t= forms.%s(choices=(%s))\n" % (name,fieldtype,choices ) )
				else:
					f.write("\t%s\t= forms.%s()\n" % (name,fieldtype) )
			f.close()
			#remove lock file
			os.remove("portal/customtypes.py.lock")
			response = "<div class='alert alert-success'><button type='button' class='close' data-dismiss='alert'>&times;</button>Custom form %s updated</div>" % type
			return HttpResponse(response)

@login_required
def customformdelete(request):
	logging.debug("prout")
	if request.method == 'POST' and request.POST.has_key('type'):
		type = request.POST['type'].capitalize()
		if os.path.exists("portal/customtypes.py.lock"):
			response = "<div class='alert alert-error'><button type='button' class='close' data-dismiss='alert'>&times;</button>customtypes  currently edited by another user</div>"
			return HttpResponse(response)
		else:
			#open lock file
			open("portal/customtypes.py.lock", 'a').close()
			types=[]
			import customtypes
			attributes=[]
			exec("form=%s()" % type)
			for attr in form.fields:
				attributes.append(attr)
			attributes.insert(0,type)
			#NOW WE NEED TO PARSE THE FILE AND REMOVE ACCORDINGLY LINES!!!!
			for line in fileinput.input("portal/customtypes.py", inplace=True):
				found = False
				for attribute in attributes:
					if attribute in line:
						found = True
						break
				if not found:
					print line,
			#remove lock file
			os.remove("portal/customtypes.py.lock")
			response = "<div class='alert alert-success'><button type='button' class='close' data-dismiss='alert'>&times;</button>Custom form %s deleted</div>" % type
			return HttpResponse(response)

#@login_required
def invoicepdf(request):
	try:
		from reportlab.pdfgen import canvas
	except:
        	information = { 'title':'Missing library' , 'details':'python-reportlab missing.Contact administrator...' }
        	return render(request, 'information.html', { 'information' : information } )
	try:
		from dateutil.relativedelta import relativedelta
	except:
        	information = { 'title':'Missing library' , 'details':'python-dateutil missing.Contact administrator...' }
        	return render(request, 'information.html', { 'information' : information } )
	if request.method == 'GET' and request.GET.has_key('id'):
			now      = datetime.now()
			nowday   = now.strftime("%d")
			nowmonth = now.strftime("%Y-%m")
			details = []
			default = Default.objects.all()[0]
			currency = default.currency
			vmid = request.GET.get('id')
			vm = VM.objects.get(id=vmid)
			price = vm.price
			virtualprovider = vm.virtualprovider.name
			name = vm.name
			createdwhen = vm.createdwhen
			month    = createdwhen.strftime("%Y-%m")
			day      = createdwhen.strftime("%d")
    			response = HttpResponse(content_type='application/pdf')
    			response['Content-Disposition'] = 'attachment; filename="%s_%s_%s"' % (now.strftime("%Y-%m-%d"),virtualprovider,vm.name)
    			p = canvas.Canvas(response)
			p.setLineWidth(.3)
			p.setFont('Helvetica', 12)
			p.drawString(30,750,'Billing information regarding VM %s' % name)
			p.drawString(30,735,"From provider %s" % virtualprovider)
			p.drawString(500,750,"Date: %s" % datetime.now().strftime("%Y-%m-%d"))
			p.drawString(275,725,'Price per day:')
			p.drawString(500,725,"%s" % vm.price+currency)
			p.line(378,723,580,723)
			p.drawString(30,703,'Owner:')
			#p.line(120,700,580,700)
			p.drawString(120,703,"%s" % vm.createdby)
			p.drawString(30,680,'Month:')
			#p.line(120,700,580,700)
			p.drawString(120,680,"Total price:")
			y = 660
			#at least this time
			if month != nowmonth:
				firstyear,firstmonth=month.split('-')
				numdays = monthrange(int(firstyear),int(firstmonth))[1]
				totaldays = int(numdays) -int(day) +1
				total = str(totaldays*price)+currency
				p.drawString(30,y,"%s" % month)
				p.drawString(120,y,total)
				y = y -20
				month = createdwhen+ relativedelta(months=1)
				month = month.strftime("%Y-%m")
				while month != nowmonth:
					month    = month.strftime("%Y-%m")
					currentyear,currentmonth=month.split('-')
					numdays = monthrange(int(currentyear),int(currentmonth))[1]
					total = str(int(numdays)*price)+currency
					p.drawString(30,y,"%s" % month)
					p.drawString(120,y,total)
					y = y -20
					month = createdwhen+ relativedelta(months=1)
					month = month.strftime("%Y-%m")
			        total = str(int(nowday)*price)+currency
				p.drawString(30,y,"%s" % month)
				p.drawString(120,y,total)
				
			else: 
				now      = datetime.now()
				nowday   = now.strftime("%d")
				nowmonth = now.strftime("%Y-%m")
				total = str(int(nowday)*price)+currency
				p.drawString(30,y,"%s" % nowmonth)
				p.drawString(120,y,total)
				y = y -20
    			p.showPage()
    			p.save()
    			return response	

@login_required
def invoice(request):
	username	  = request.user.username
	username          = User.objects.filter(username=username)[0]
	try:
		from dateutil.relativedelta import relativedelta
	except:
        	information = { 'title':'Missing library' , 'details':'python-dateutil missing.Contact administrator...' }
        	return render(request, 'information.html', { 'information' : information } )
	if request.method == 'GET' and request.GET.has_key('id'):
			default = Default.objects.all()[0]
			details = []
			vmid = request.GET.get('id')
			vm = VM.objects.get(id=vmid)
			virtualprovider = vm.virtualprovider.name
			price = vm.price
			if not price:
        			information = { 'title':'Missing information' , 'details':'no invoice available for this VM' }
        			return render(request, 'information.html', { 'information' : information } )
			createdwhen = vm.createdwhen
			month    = createdwhen.strftime("%Y-%m")
			day      = createdwhen.strftime("%d")
			now      = datetime.now()
			nowday   = now.strftime("%d")
			nowmonth = now.strftime("%Y-%m")
			#at least this time
			if month != nowmonth:
				firstyear,firstmonth=month.split('-')
				numdays = monthrange(int(firstyear),int(firstmonth))[1]
				totaldays = int(numdays) -int(day) +1
				total = totaldays*price
				details.append({ 'month': month , 'total' : total })
				month = createdwhen+ relativedelta(months=1)
				month = month.strftime("%Y-%m")
				while month != nowmonth:
					month    = month.strftime("%Y-%m")
					currentyear,currentmonth=month.split('-')
					numdays = monthrange(int(currentyear),int(currentmonth))[1]
					total = int(numdays)*price
					details.append({ 'month': month , 'total' : total })
					month = createdwhen+ relativedelta(months=1)
					month = month.strftime("%Y-%m")
			        total = int(nowday)*price
				details.append({ 'month': month , 'total' : total  })
				
			else: 
				now      = datetime.now()
				nowday   = now.strftime("%d")
				nowmonth = now.strftime("%Y-%m")
				total = int(nowday)*price
				details.append({ 'month': nowmonth , 'total' : nowday  })
                	return render(request, 'invoice.html', { 'vm': vm , 'username': username  , 'details': details , 'default': default } )


@login_required
def profilecopy(request):
        logging.debug("prout")
        username          = request.user.username
        username          = User.objects.filter(username=username)[0]
        groups            = username.groups
        profiles=Profile.objects.all()
        if request.method == 'POST' and request.is_ajax():
		if request.POST.has_key('newprofile'):
			profile = request.POST['profile']
            		profile=Profile.objects.get(name=profile)
			oldname = profile.name
			newprofile = request.POST['newprofile']
            		exist=Profile.objects.filter(name=newprofile)
			if exist:
            			return HttpResponse("<div class='alert alert-error' ><button type='button' class='close' data-dismiss='alert'>&times;</button>profile allready existing</div>")
			profile.name = newprofile
			profile.cobblerprofile = oldname
			profile.pk = None
			profile.save()
            		return HttpResponse("<div class='alert alert-success' ><button type='button' class='close' data-dismiss='alert'>&times;</button>profile successfully copied</div>")
		else:
            		profile = request.POST['profile']
            		profile=Profile.objects.get(name=profile)
            		cobblerprofile=profile.name
            		providers = ""
            		if profile.cobblerprofile:
                		cobblerprofile=profile.cobblerprofile
            		return HttpResponse("<div class='alert alert-success' ><button type='button' class='close' data-dismiss='alert'>&times;</button>Cobbler Profile: %s<p><p>Datacenter: %s<p>Cluster: %s<p>Number of cpus: %s<p>Memory: %sMo<p>Guestid: %s<p>Disksize first disk : %sGb<p>Number of network interfaces: %s<p>Foreman Enabled: %s<p>Cobbler Enabled:%s<p>Isos List Enabled: %s<p>Virtual Provider: %s<p>Physical Provider: %s<p></div>" % (cobblerprofile,profile.datacenter,profile.clu,profile.numcpu,profile.memory,profile.guestid,profile.disksize1,profile.numinterfaces,profile.foreman,profile.cobbler,profile.iso,profile.virtualprovider,profile.physicalprovider ))
        elif username.is_staff:
            profiles = Profile.objects.all()
            if not profiles:
                information = { 'title':'Missing elements' , 'details':'Create profiles first...' }
                return render(request, 'information.html', { 'information' : information } )
            else:
                return render(request, 'profilecopy.html', { 'profiles': profiles , 'username': username } )





