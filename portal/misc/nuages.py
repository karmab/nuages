#!/usr/bin/python
"""
wrapper around the nuages REST api
"""

import ConfigParser
import optparse
import os
import requests
import sys
import simplejson as json

__author__ = "Karim Boumedhel"
__credits__ = ["Karim Boumedhel"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Karim Boumedhel"
__email__ = "karim.boumedhel@gmail.com"
__status__ = "Production"

ERR_NONUAGEFILE = "You need to create a correct nuages.ini file in your home directory.Check documentation"

class Nuage:
    def __init__(self, host, port, user, password,secure=False):
        host          = host.encode('ascii')
        port          = str(port).encode('ascii')
        user          = user.encode('ascii')
        password      = password.encode('ascii')
        self.host     = host
        self.port     = port
        self.user     = user
        self.password = password
        self.headers   = {'content-type': 'application/json', 'Accept': 'application/json' }
        #if secure:
        #self.protocol = 'https'
        #else:
        self.protocol = 'http'
    #def create(self,name,profile):
    def create(self, name, profile, storage=None, ip1=None, ip2=None, ip3=None, ip4=None, hostgroup=None, iso=None):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm" % (protocol, host, port)
        data = { "profile" : "/nuages/api/v1/profile/%s" % profile , "name" : name }
        if ip1:
            data['ip1']= ip1
        if ip2:
            data['ip2'] = ip2
        if ip3:
            data['ip3'] = ip3
        if ip4:
            data['ip4'] = ip4
        if hostgroup:
            data['hostgroup'] = hostgroup
        if iso:
            data['iso'] = iso
        if parameters:
            data['parameters'] = parameters
        if puppetclasses:
            data['puppetclasses'] = puppetclasses
        if storage:
            data['storagedomain'] = storage
        r = requests.post(url,verify=False, data=json.dumps(data), headers=headers, auth=(user,password))
        return r.text
    def storages(self):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/storage" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        return results
    def vms(self):
        allvms = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for vm in results:
            allvms.append(vm['name'])
        return allvms
    def profiles(self):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/profile" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        return results
    def profile(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/profile/%s" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()
        return results
    def cobblerproviders(self):
        cps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/cobblerprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for cp in results:
            cps.append(cp['name'])
        return cps
    def foremanproviders(self):
        fps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/cobblerprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for fp in results:
            fps.append(fp['name'])
        return fps
    def physicalproviders(self):
        pps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/physicalprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for pp in results:
            pps.append(pp['name'])
        return pps
    def console(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/console" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def delete(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s" % (protocol, host, port, name)
        r = requests.delete(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def kill(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/kill" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def start(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/start" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def stop(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/stop" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def vm(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        return r.json()
    def virtualproviders(self):
        vps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/virtualprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for vp in results:
            vps.append(vp['name'])
        return vps
    def virtualprovider(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/virtualprovider/%s" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()
        return results
    def storage(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/virtualprovider/%s/storage" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()
        return results

if __name__ == '__main__':
    usage = 'wrapper around nuages api'
    version = '1.1'
    parser = optparse.OptionParser('Usage: %prog [options] vmname',version=version)
    actiongroup = optparse.OptionGroup(parser, 'Action options')
    actiongroup.add_option('-o', '--console', dest='console', action='store_true', help='get console')
    actiongroup.add_option('-s', '--start', dest='start', action='store_true', help='start vm')
    actiongroup.add_option('-w', '--stop', dest='stop', action='store_true', help='stop vm')
    parser.add_option_group(actiongroup)
    creationgroup = optparse.OptionGroup(parser, 'Creation options')
    creationgroup.add_option('-d', '--delete', dest='delete', action='store_true', help='delete vm')
    creationgroup.add_option('-k', '--kill', dest='kill', action='store_true', help='kill vm')
    creationgroup.add_option("-p", "--profile", dest="profile",type="string", help="specify Profile")
    creationgroup.add_option('-n', '--create', dest='create', action='store_true', help='create vm')
    creationgroup.add_option("-1", "--ip1", dest="ip1", type="string", help="Specify First IP")
    creationgroup.add_option("-2", "--ip2", dest="ip2", type="string", help="Specify Second IP")
    creationgroup.add_option("-3", "--ip3", dest="ip3", type="string", help="Specify Third IP")
    creationgroup.add_option("-4", "--ip4", dest="ip4", type="string", help="Specify Fourth IP")
    creationgroup.add_option("-H", "--hostgroup", dest="hostgroup", type="string", help="Specify hostgroup")
    creationgroup.add_option("-I", "--iso", dest="iso", type="string", help="Specify iso")
    creationgroup.add_option("-x", "--parameters", dest="parameters", type="string", help="Specify parameters, by spaces")
    creationgroup.add_option("-y", "--puppetclasses", dest="puppetclasses", type="string", help="Specify puppetclasses, separated by commas")
    parser.add_option_group(creationgroup)
    listinggroup = optparse.OptionGroup(parser, "Creation options")
    listinggroup.add_option('-L', '--listclients', dest="listclients", action='store_true', help='list available clients')
    listinggroup.add_option('-c', '--cobblerproviders', dest='cobblerproviders', action='store_true', help='list cobblerproviders')
    listinggroup.add_option('-f', '--foremanproviders', dest='foremanproviders', action='store_true', help='list foremanproviders')
    listinggroup.add_option('-l', '--profiles', dest='profiles', action='store_true', help='list available profiles')
    listinggroup.add_option('-S', '--storage', dest='storages', action='store_true', help='list available storage')
    listinggroup.add_option('-v', '--virtualproviders', dest='virtualproviders', action='store_true', help='list virtual providers')
    listinggroup.add_option('-Q', '--physicalproviders', dest='physicalproviders', action='store_true', help='list physical providers')
    listinggroup.add_option('-V', '--vms', dest='vms', action='store_true', help='list all vms')
    listinggroup.add_option("-z", "--virtualprovider", dest="virtualprovider", type="string", help="Specify virtualprovider")
    parser.add_option_group(listinggroup)
    parser.add_option("-C", "--client", dest="client", type="string", help="Specify Client")
    parser.add_option("-9", "--switchclient", dest="switchclient", type="string", help="Switch default client")
    (options, args) = parser.parse_args()
    client = options.client
    profile = options.profile
    profiles = options.profiles
    listclients = options.listclients
    storages = options.storages
    vms = options.vms
    cobblerproviders = options.cobblerproviders
    foremanproviders = options.foremanproviders
    physicalproviders = options.physicalproviders
    virtualproviders = options.virtualproviders
    virtualprovider = options.virtualprovider
    switchclient = options.switchclient
    console = options.console
    start = options.start
    create = options.create
    kill = options.kill
    delete = options.delete
    stop = options.stop
    ip1 = options.ip1
    ip2 = options.ip2
    ip3 = options.ip3
    ip4 = options.ip4
    hostgroup = options.hostgroup
    iso = options.iso
    parameters = options.parameters
    puppetclasses = options.puppetclasses
    nuageconffile = "%s/nuages.ini" % (os.environ['HOME'])
    #parse nuage client auth file
    if not os.path.exists(nuageconffile):
        print "Missing %s in your  home directory.Check documentation" % nuageconffile
        sys.exit(1)
    try:
        c = ConfigParser.ConfigParser()
        c.read(nuageconffile)
        nuages = {}
        default = {}
        for cli in c.sections():
            for option in  c.options(cli):
                if cli=="default":
                    default[option] = c.get(cli,option)
                    continue
                if not nuages.has_key(cli):
                    nuages[cli] = {option : c.get(cli,option)}
                else:
                    nuages[cli][option] = c.get(cli,option)
    except:
        print ERR_NONUAGEFILE
        os._exit(1)

    if listclients:
        print "Available Clients:"
        for cli in  sorted(nuages):
            print cli
        if default.has_key("client"):
            print "Current default client is: %s" % (default["client"])
        sys.exit(0)

    if switchclient:
        if switchclient not in nuages.keys():
            print "Client not defined...Leaving"
        else:
            mod = open(nuageconffile).readlines()
            f = open(nuageconffile, "w")
            for line in mod:
                if line.startswith("client"):
                    f.write("client=%s\n" % switchclient)
                else:
                    f.write(line)
            f.close()
            print "Default Client set to %s" % (switchclient)
        sys.exit(0)

    if not client:
        try:
            client = default['client']
        except:
            print "No client defined as default in your ini file or specified in command line"
            os._exit(1)

    try:
        host     = nuages[client]["host"]
        port     = nuages[client]["port"]
        user     = nuages[client]["user"]
        password = nuages[client]["password"]
    except KeyError,e:
        print "Problem parsing nuage ini file:Missing parameter %s" % e
        os._exit(1)

    n  = Nuage(host, port, user, password)
    if profiles:
        for profile in sorted(n.profiles(), key=lambda profile: profile['name']):
            print profile['name']
        sys.exit(0)
    if storages:
        for storage in sorted(n.storages(), key=lambda storage: storage['name']):
            print storage['name']
        sys.exit(0)
    if cobblerproviders:
        for cp in sorted(n.cobblerproviders()):
            print cp
        sys.exit(0)
    if foremanproviders:
        for fp in sorted(n.foremanproviders()):
            print fp
        sys.exit(0)
    if physicalproviders:
        for pp in sorted(n.physicalproviders()):
            print pp
        sys.exit(0)
    if virtualproviders:
        for vp in sorted(n.virtualproviders()):
            print vp
        sys.exit(0)
    if vms:
        for vm in sorted(n.vms()):
            print vm
        sys.exit(0)
    if profile:
        profiles = []
        for prof in sorted(n.profiles(), key=lambda profile: profile['name']):
            profiles.append(prof['name'])
        if not profile in profiles:
            print "Profile %s not found" % profile
            sys.exit(0)
        results = n.profile(profile)
        for attribute in sorted(results):
            if attribute in ['resource_uri'] or results[attribute]=='' or results[attribute]==None:
                continue
            print "%s: %s" % (attribute, str(results[attribute]).replace("/nuages/api/v1/%s/" % attribute,''))
        sys.exit(0)
    if virtualprovider:
        virtualproviders = n.virtualproviders()
        if not virtualprovider in virtualproviders:
            print "VirtualProvider %s not found" % virtualprovider
            sys.exit(0)
        results = n.virtualprovider(virtualprovider)
        for attribute in sorted(results):
            if attribute in ['resource_uri'] or results[attribute]=='' or results[attribute]==None:
                continue
            print "%s: %s" % (attribute, str(results[attribute]).replace("/nuages/api/v1/%s/" % attribute,''))
        results = n.storage(virtualprovider)
        print "SD\tAvailable\tUsed"
        for result in results:
            print "%s\t%sGB\t\t%sGB" % (result, results[result][1], results[result][0])
        sys.exit(0)
    if len(args) != 1:
        print 'Name required'
        sys.exit(0)
    name = args[0]
    if start:
        n.start(name)
        print "VM %s started" % name
    if stop:
        n.stop(name)
        print "VM %s stopped" % name
        sys.exit(0)
    if delete:
        n.delete(name)
        print "VM %s deleted" % name
        sys.exit(0)
    if kill:
        n.kill(name)
        n.delete(name)
        print "VM %s killed" % name
        sys.exit(0)
    if console:
        results = n.console(name)
        baseurl = "http://%s:%s" % (host, port)
        print "%s%s" % (baseurl, results)
        sys.exit(0)
    if create and profile:
        profiles = []
        for prof in sorted(n.profiles(), key=lambda profile: profile['name']):
            profiles.append(prof['name'])
        if not profile in profiles:
            print "Profile %s not found" % profile
            sys.exit(0)
        details = n.profile(profile)
        if not details.autostorage and not storage:
            print "This profile requires a storagedomain to be set"
            sys.exit(0)
        results = n.create(name=name, profile=profile, storage=storage, ip1=ip1, ip2=ip2, ip3=ip3, ip4=ip4, hostgroup=hostgroup, iso=iso, parameters=parameters, puppetclasses=puppetclasses)
        print "VM %s created" % name
    results = n.vm(name)
    for attribute in sorted(results):
        if attribute in ['create','iso','resource_uri','status'] or results[attribute]=='' or results[attribute]==None:
            continue
        print "%s: %s" % (attribute, str(results[attribute]).replace("/nuages/api/v1/%s/" % attribute,''))
