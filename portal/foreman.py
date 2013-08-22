import datetime
import json
import os
import requests
import simplejson
import sys
import time

hostname=os.environ["HOSTNAME"]

#helper functions
def foremando(url, actiontype=None, postdata=None, v2=False, user=None, password=None):
 headers = {'content-type': 'application/json', 'Accept': 'application/json,version=2' }
 #get environments
 envs={}
 if user and password:
  user     = user.encode('ascii')
  password = password.encode('ascii')
 #c.setopt(pycurl.SSL_VERIFYPEER, False)
 #c.setopt(pycurl.SSL_VERIFYHOST, False)
 if actiontype=="POST":
 	r = requests.post(url,headers=headers,auth=(user,password),data=json.dumps(postdata))
 elif actiontype=="DELETE":
 	r = requests.delete(url,headers=headers,auth=(user,password),data=postdata)
 elif actiontype=="PUT":
 	r = requests.put(url,headers=headers,auth=(user,password),data=postdata)
 else:
 	r = requests.get(url,headers=headers,auth=(user,password))
 try:
  result = r.json()
  result = eval(str(result))
  return result
 except:
  return None

def foremangetid(host,port,user,password, searchtype, searchname):
 if searchtype=="puppet":
  url = "http://%s:%s/api/smart_proxies?type=%s"  % (host, port,searchtype)
  result = foremando(url)
  return result[0]["smart_proxy"]["id"]
 else:
  url = "http://%s:%s/api/%s/%s" % (host, port,searchtype, searchname)
  result = foremando(url=url, user=user, password=password)
 if searchtype.endswith("es") and searchtype != "architectures":
  shortname = searchtype[:-2]
 else:
  shortname = searchtype[:-1]
 return str(result[shortname]["id"])

#VM CREATION IN FOREMAN
class Foreman:
	def __init__(self,host, port,user, password):
		host=host.encode('ascii')
		port=str(port).encode('ascii')
		user=user.encode('ascii')
		password=password.encode('ascii')
		self.host=host
		self.port=port
		self.user=user
		self.password=password
	def delete(self, name, dns=None):
		host, user , password = self.host,self.user, self.password
		name=name.encode('ascii')
 		if dns:
			dns=dns.encode('ascii')
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
	def create(self,name, dns, ip, mac=None,osid=None, envid=None, archid="x86_64", puppetid=None, ptableid=None, powerup=None, memory=None, core=None, computeid=None, hostgroup=None):
		host, port, user , password = self.host,self.port,self.user, self.password
		name=name.encode('ascii')
		dns=dns.encode('ascii')
 		if not envid:
     			envid = "production"
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
 		url = "http://%s:%s/hosts" % (host,port)
 		if dns:
     			name = "%s.%s" % (name, dns)
 		if osid:
     			osid = foremangetid(host,port,user,password,"operatingsystems", osid)
		envid = foremangetid(host,port,user,password, "environments", envid)
 		if archid:
     			archid = foremangetid(host,port,user,password, "architectures", archid)
 		if puppetid:
     			puppetid = foremangetid(host,port,user,password, "puppet", puppetid)
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
  			computeid = foremangetid(host,port,user,password, "compute_resources", computeid)
  			postdata["host"]["compute_resource_id"] = computeid
 		if hostgroup:
  			hostgroupid = foremangetid(host,port,user,password, "hostgroups", hostgroup)
  			postdata["host"]["hostgroup_id"] = hostgroupid
 		if ptableid:
  			ptableid = foremangetid(host,port,user,password, "ptables", ptableid)
  			postdata["host"]["ptable_id"] = hostgroupid
 		result = foremando(url=url, actiontype="POST", postdata=postdata, user=user, password=password)
 		if not result.has_key('errors'):
  			now    = datetime.datetime.now()
  			header = "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  			print header+"%s created in Foreman\n" % name
 		else:
  			now    = datetime.datetime.now()
 			header = "%s %s " % (now.strftime("%b %d %H:%M:%S"), hostname)
  			print header+"%s not created in Foreman because %s\n" % (name, result["errors"][0])

	def addclasses(self,name,dns,classes):
		return "prout"
		name=name.encode('ascii')
		dns=dns.encode('ascii')
		#should be a reflection of
		#curl -X POST -d "{\"puppetclass_id\":2}" -H "Content-Type:application/json" -H "Accept:application/json,version=2" http://192.168.8.8/api/hosts/10/puppetclass_ids
		host, port, user , password = self.host,self.port,self.user, self.password
 		classes = classes.split(",")
 		for classe in classes:
  			classid = foremangetid(host,user,password, "puppetclasses", classe) 
  			url = "http://%s:%s/api/hosts/%s/puppetclass_ids" % (host,port,name)
  			postdata = {"puppetclass_id": classid}
  			foremando(url=url, actiontype="POST", postdata=postdata, v2=True, user=user, password=password)

	def addparameters(self,name,dns,parameters):
		return "prout"
		host, port, user , password = self.host,self.port,self.user, self.password
		name=name.encode('ascii')
		dns=dns.encode('ascii')
 		parameters = parameters.split(" ")
 		for parameter in parameters:
  			parameter,value = parameter.split("=")
  			parameterid = foremangetid(foreman, "parameters", parameter)
  			url = "http://%s:%s/api/hosts/%s/parameter_ids" % (host,port, name)
  			postdata = {"parameter_id": parameterid}
  			foremando(url=url, actiontype="POST", postdata=postdata, v2=True, user=user, password=password)
	def hostgroups(self,environment):
		host, port, user , password = self.host,self.port,self.user, self.password
                url="http://%s:%s/api/hostgroups?search=environment+=+%s" % (host,port,environment)
		res= foremando(url=url, user=user, password=password)
		results={}
		for  r in res:
 			info=r.values()[0]
 			name=info["name"]
 			del info["name"]
 			results[name]=info
 		return sorted(results)

	def classes(self,environment):
		host, port, user , password = self.host,self.port,self.user, self.password
                url="http://%s:%s/api/puppetclasses?search=environment+=+%s" % (host,port,environment)
		res= foremando(url=url, user=user, password=password)
		results=[]
		for  classe in res.keys():
			results.append(classe)
 		return sorted(results)

        def exists(self,name):
		host, port, user , password = self.host,self.port,self.user, self.password
                url="http://%s:%s/api/hosts"  % (host,port)
                res= foremando(url=url, user=user, password=password)
                results={}
                for  r in res:
                        info=r.values()[0]
                        if info["name"]== name:
				return True
                return False
