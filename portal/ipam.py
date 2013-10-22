import json
import requests
import sys
class Ipam:
    def __init__(self, host, port, username, password):
        self.host, self.port, self.username, self.password = host, port, username, password

    def getinfo(self):
        host, port, username, password = self.host, self.port, self.username, self.password
        url = "http://%s:%s" % (host, port)
        headers = {'content-type': 'application/json', 'Accept': 'application/json,version=' }
        #get environments
        envs = {}
        envurl = "%s/environments" % url
        r = requests.get(envurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name = r['code']
            id = r['id']
            envs[name] = id
        #get roles
        roles = {}
        rolesurl = "%s/roles" % url
        r = requests.get(rolesurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name = r['code']
            id = r['id']
            roles[name] = id
        #get operating_systems
        operatingsystems={}
        operatingsystemsurl = "%s/operating_systems" % url
        r = requests.get(operatingsystemsurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name = r['code']
            id = r['id']
            operatingsystems[name] = id
        #get dnszones
        dnszones = {}
        dnszonesurl = "%s/dnszones" % url
        r = requests.get(dnszonesurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name = r['name']
            id = r['id']
            dnszones[name] = id
        #get mtypes
        mtypes = {}
        mtypesurl = "%s/mtypes" % url
        r = requests.get(mtypesurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name = r['name']
            id = r['id']
            mtypes[name] = id
        #get vlans
        vlans = {}
        vlansurl = "%s/vlans" % url
        r = requests.get(vlansurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name = r['name']
            id = r['id']
            vlans[name] = id
        self.envs, self.roles, self.operatingsystems, self.dnszones, self.mtypes, self.vlans = envs, roles, operatingsystems, dnszones,mtypes,vlans
        #get projects
        projects = {}
        projectsurl = "%s/projects" % url
        r = requests.get(projectsurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            name=r['name']
            id=r['id']
            projects[name]=id
        self.envs, self.roles, self.operatingsystems, self.dnszones, self.mtypes, self.vlans, self.projects = envs, roles, operatingsystems, dnszones,mtypes,vlans,projects


    def create(self, hostname=None, virtual=True, environment='PRO', role='UT', operatingsystem='L', dnszone='.ib', mtype='standalone_server', project=None):
        host, port, username, password = self.host, self.port, self.username, self.password
        createurl = "http://%s:%s/machines/" % (host, port)
        environment = "http://%s/environments/%d/" % (host, self.envs[environment])
        role = "http://%s/roles/%d/" % (host, self.roles[role])
        operatingsystem = "http://%s/operating_systems/%d/" % (host, self.operatingsystems[operatingsystem])
        dnszone = "http://%s/dnszones/%d/" % (host, self.dnszones[dnszone])
        mtype= "http://%s/mtypes/%d/" % (host, self.mtypes[mtype])
        if project:
            project= "http://%s/projects/%d/" % (host,self.projects[project])
        headers = {'content-type': 'application/json', 'Accept': 'application/json,version=' }
        postdata = {'environment': environment , 'virtual': virtual , 'role' : role , 'operating_system' : operatingsystem , 'dns_zone' : dnszone , 'mtype' : mtype }
        if project:
            postdata['project'] = project
        if hostname:
            postdata['hostname'] = hostname
        r = requests.post(createurl, verify=False, postdata, auth=(username, password))
        results = r.json()
        return hostname, results["id"]


    def getnetwork(self, machineid, vlan='MAN1', numinterfaces=1):
        host, port, username, password = self.host, self.port, self.username, self.password
        ipurl = "http://%s:%s/ifaces/" % (host,port)
        machineid = "http://%s/machines/%d/" % (host, machineid)
        vlan= "http://%s/vlans/%d/" % (host, self.vlans[vlan])
        postdata = { 'machine': machineid , 'vlan': vlan }
        r = requests.post(ipurl, verify=False, postdata, auth=(username, password))
        results = r.json()
        return results['ip'],results['mask'],results['gw']

    def setiface(self,hostname,interface):
        host, port, username, password = self.host, self.port, self.username, self.password
        headers = {'content-type': 'application/json', 'Accept': 'application/json,version=' }
        #get machineid
        machineid = None
        found = False
        nexturl = "http://%s:%s/machines/" % (host, port)
        while not found:
            r = requests.get(nexturl, verify=False, headers=headers, auth=(username, password))
            results = r.json()
            nexturl = results['next']
            results = results['results']
            for r in results:
                if r['hostname'] == hostname:
                    machineid = r['id']
                    found=True
                    break
        #get ifaceid
        ipurl = "http://%s:%s/ifaces/" % (host, port)
        r = requests.get(ipurl, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        results = results['results']
        for r in results:
            if r['machine'].endswith("/%s/" % machineid):
                ifaceid = r['id']
                vlan = r['vlan']
                ip = r['ip']
                gw = r['gw']
                mask = r['mask']
        #get vlan name
        r = requests.get(vlan, verify=False, headers=headers, auth=(username, password))
        results = r.json()
        vlanname = results['name']
        #update interface
        machineinfo = "http://%s/machines/%d/" % (host, machineid)
        postdata = { 'machine': machineinfo , 'ip' : ip , 'gw': gw , 'mask': mask , 'vlan': vlan , 'name' : "%s_%s" % (interface, vlanname) }
        ipurl="http://%s:%s/ifaces/%d/" % (host, port, ifaceid)
        r = requests.put(ipurl,verify=False, postdata, auth=(username, password))
        #results = r.json()
        #return results
