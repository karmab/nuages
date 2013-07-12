import datetime
import pycurl
import os
import simplejson
import sys
import time
import StringIO

hostname=os.environ["HOSTNAME"]
pwd = os.environ["PWD"]
#log = open("%s/nuages.log" % pwd,"a")

def foremando(url, actiontype=None, postdata=None, v2=False, user=None, password=None):
 if postdata:
     postdata="%s" % str(postdata).replace("'",'"')
 c = pycurl.Curl()
 b = StringIO.StringIO()
 c.setopt(pycurl.URL, url)
# if v2:
#  c.setopt(pycurl.HTTPHEADER, [ "Content-type: application/json","Accept: application/json,version=2"])
# else:
#  c.setopt(pycurl.HTTPHEADER, [ "Content-type: application/json","Accept: application/json"])
 c.setopt(pycurl.HTTPHEADER, [ "Content-type: application/json","Accept: application/json,version=2"])
 c.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_BASIC)
 if user and password:
     #c.setopt(pycurl.USERPWD, "%s:%s" % (user,password))
     c.setopt(pycurl.USERPWD, ("%s:%s" % (user,password)).encode("ascii"))
 c.setopt(pycurl.SSL_VERIFYPEER, False)
 c.setopt(pycurl.SSL_VERIFYHOST, False)
 if actiontype=="POST":
  c.setopt( pycurl.POST, 1 )
  c.setopt(pycurl.POSTFIELDS,postdata)
 elif actiontype=="DELETE":
  c.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
 elif actiontype=="PUT":
  c.setopt( pycurl.CUSTOMREQUEST, "PUT" )
  c.setopt(pycurl.POSTFIELDS, postdata)
 #else:
 c.setopt(pycurl.WRITEFUNCTION, b.write)
 c.perform()
 #if not actiontype in ["POST","PUT","DELETE"]:
 try:
  result = b.getvalue()
  result = simplejson.loads(result)
  result = eval(str(result))
  return result
 except:
  return None

def foremangetid(host,user,password, searchtype, searchname):
 if searchtype=="puppet":
  url = "http://%s/api/smart_proxies?type=%s"  % (host, searchtype)
  result = foremando(url)
  return result[0]["smart_proxy"]["id"]
 else:
  url = "http://%s/api/%s/%s" % (host, searchtype, searchname)
  result = foremando(url=url, user=user, password=password)
 if searchtype.endswith("es"):
  shortname = searchtype[:-2]
 else:
  shortname = searchtype[:-1]
 return str(result[shortname]["id"])

def foremancreate(host, user, password, name, dns, osid=None, envid=None, archid=None, puppetid=None, ptableid=None, powerup=None, ip=None, mac=None, memory=None, core=None, computeid=None, hostgroup=None):
 url = "http://%s/hosts" % (host)
 if dns:
     name = "%s.%s" % (name, dns)
 if osid:
     osid = foremangetid(host,user,password,"operatingsystems", osid)
 if not envid:
     envid = "production"
 if envid:
     envid = foremangetid(host,user,password, "environments", envid)
 if archid:
     archid = foremangetid(host,user,password, "architectures", archid)
 if puppetid:
     puppetid = foremangetid(host,user,password, "puppet", puppetid)
 postdata = {}
 postdata["host"] = {"name":name}
 if osid:
     postdata["host"]["operatingsystem_id"] = osid
 if envid:
     postdata["host"]["environment_id"] = envid
 if archid:
     postdata["host"]["architecture_id"] = envid
 if puppetid:
     postdata["host"]["puppet_proxy_id"] = puppetid
 if ptableid:
     postdata["host"]["ptable_id"] = ptableid
 if ip:
     postdata["host"]["ip"] = ip
 if mac:
     postdata["host"]["mac"] = mac
 if computeid:
  computeid = foremangetid(host,user,password, "compute_resources", computeid)
  postdata["host"]["compute_resource_id"] = computeid
 if hostgroup:
  hostgroupid = foremangetid(host,user,password, "hostgroups", hostgroup)
  postdata["host"]["hostgroup_id"] = hostgroupid
 if ptableid:
  ptableid = foremangetid(host,user,password, "ptables", ptableid)
  postdata["host"]["ptable_id"] = hostgroupid
 postdata = "%s" % str(postdata).replace("'",'"')
 result = foremando(url=url, actiontype="POST", postdata=postdata, user=user, password=password)
 if not result.has_key('errors'):
  	now    = datetime.datetime.now()
  	header = "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  	print header+"%s created in Foreman\n" % name
 else:
  	now    = datetime.datetime.now()
 	header = "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  	print header+"%s not created in Foreman because %s\n" % (name, result["errors"][0])
 

def foremandelete(host,user,password, name, dns=None):
 if dns:
     name = "%s.%s" % (name, dns)
 url = "http://%s/hosts/%s" % (host, name) 
 result = foremando(url=url, actiontype="DELETE", user=user, password=password)
 if result:
  now = datetime.datetime.now()
  header= "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  print header+"%s deleted in Foreman\n" % name
 else:
  now = datetime.datetime.now()
  header= "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  print header+"Nothing to do in foreman\n"

#should be a reflection of
#curl -X POST -d "{\"puppetclass_id\":2}" -H "Content-Type:application/json" -H "Accept:application/json,version=2" http://192.168.8.8/api/hosts/10/puppetclass_ids
def foremanaddpuppetclass(host,user,password, name, puppetclasses):
 puppetclasses = puppetclasses.split(",")
 for puppetclass in puppetclasses:
  puppetclassid = foremangetid(host, "puppetclasses", puppetclass) 
  #nameid = foremangetid(host, "hosts", name)
  url = "http://%s/api/hosts/%s/puppetclass_ids" % (host,name)
  postdata = {"puppetclass_id": puppetclassid}
  foremando(url=url, actiontype="POST", postdata=postdata, v2=True, user=user, password=password)


def foremanaddparameter(host,user,password,name, puppetparameters):
 puppetparameters = puppetparameters.split(",")
 for puppetparameter in puppetparameters:
  parameter,value = puppetparameter.split("=")
  parameterid = foremangetid(foreman, "parameters", parameter)
  url = "http://%s/api/hosts/%s/parameter_ids" % (host, name)
  postdata = {"parameter_id": parameterid}
  foremando(url=url, actiontype="POST", postdata=postdata, v2=True, user=user, password=password)

#VM CREATION IN FOREMAN
class Foreman:
	def __init__(self,host, user, password, name=None, dns=None, ip=None, mac=None,osid=None, envid=None, archid=None, puppetid=None, ptableid=None,powerup=None,memory=None,core=None,computeid=None,hostgroup=None):
		host=host.encode('ascii')
		user=user.encode('ascii')
		password=password.encode('ascii')
		self.host=host
		self.user=user
		self.password=password
		if name:
			name=name.encode('ascii')
		if dns:
			dns=dns.encode('ascii')
		if ip:
			ip=ip.encode('ascii')
		if mac:
			mac=mac.encode('ascii')
		if osid:
			osid=osid.encode('ascii')
		if envid:
			envid=envid.encode('ascii')
		if archid:
			archid=archid.encode('ascii')
		if puppetid:
			puppetid=puppetid.encode('ascii')
		if ptableid:
			ptableid=ptableid.encode('ascii')
		if powerup:
			powerup=powerup.encode('ascii')
		if memory:
			memory=memory.encode('ascii')
		if core:
			core=core.encode('ascii')
		if computeid:
			computeid=computeid.encode('ascii')
		if hostgroup:
			hostgroup=hostgroup.encode('ascii')
		if name:
			foremancreate(host=host,user=user,password=password,name=name, dns=dns, ip=ip, mac=mac,osid=osid, envid=envid, archid=archid, puppetid=puppetid, ptableid=ptableid, powerup=powerup, memory=memory, core=core, computeid=computeid, hostgroup=hostgroup)
	def addpuppetclasses(host,user,password,name,puppetclasses):
    		foremanaddpuppetclass(host=host,user=user,password=password,name=name,puppetclasses=puppetclasses)

	def hostgroups(self):
		url="http://%s/api/hostgroups"  % (self.host)
		res= foremando(url=url, user=self.user, password=self.password)
		results={}
		for  r in res:
 			info=r.values()[0]
 			name=info["name"]
 			del info["name"]
 			results[name]=info
 		return sorted(results)

        def exists(self,name):
                url="http://%s/api/hosts"  % (self.host)
                res= foremando(url=url, user=self.user, password=self.password)
                results={}
                for  r in res:
                        info=r.values()[0]
                        if info["name"]== name:
				return True
                return False

	def delete(self, name, dns=None):
		name=name.encode('ascii')
 		if dns:
			dns=dns.encode('ascii')
     			name = "%s.%s" % (name, dns)
 		url = "http://%s/hosts/%s" % (self.host, name)
 		result = foremando(url=url, actiontype="DELETE", user=self.user, password=self.password)
 		if result:
  			now = datetime.datetime.now()
  			header= "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  			print header+"%s deleted in Foreman\n" % name
 		else:
  			now = datetime.datetime.now()
  			header= "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  			print header+"Nothing to do in foreman\n"
		return True
