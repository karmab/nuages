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

def checkargs(args):
    if len(args) != 1:
        print 'Name required'
        sys.exit(0)
    return args[0]

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
        if secure:
            self.protocol = 'https'
        else:
            self.protocol = 'http'
    def create(self, profile, name=None, storage=None, ip1=None, ip2=None, ip3=None, ip4=None, hostgroup=None, iso=None, parameters=None, puppetclasses=None):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm" % (protocol, host, port)
        data = { "profile" : "/nuages/api/v1/profile/%s" % profile }
        if name:
            data['name']= name
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
    def cobblerproviders(self):
        cps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/cobblerprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for cp in results:
            cps.append(cp['name'])
        return cps
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
    def deletestack(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack/%s" % (protocol, host, port, name)
        r = requests.delete(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def foremanproviders(self):
        fps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/cobblerprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for fp in results:
            fps.append(fp['name'])
        return fps
    def kill(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/kill" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def killstack(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack/%s/kill" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def physicalproviders(self):
        pps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/physicalprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for pp in results:
            pps.append(pp['name'])
        return pps
    def profile(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/profile/%s" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()
        return results
    def profiles(self):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/profile" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        return results
    def showstack(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack/%s/show" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def stack(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack/%s" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()
        return results
    def stacks(self):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        return results
    def start(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/start" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def startstack(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack/%s/start" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def status(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/status" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def stop(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/stop" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def stopstack(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/stack/%s/stop" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def storage(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/virtualprovider/%s/storage" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()
        return results
    def storages(self):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/storage" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        return results
    def vm(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s" % (protocol, host, port, name)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        return r.json()
    def vms(self):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        return results
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
    creationgroup.add_option("-z", "--storage", dest="storage", type="string", help="Specify storage, used when creating VM")
    parser.add_option_group(creationgroup)
    listinggroup = optparse.OptionGroup(parser, "Creation options")
    listinggroup.add_option('-L', '--listclients', dest="listclients", action='store_true', help='list available clients')
    listinggroup.add_option('-c', '--cobblerproviders', dest='cobblerproviders', action='store_true', help='list cobblerproviders')
    listinggroup.add_option('-f', '--foremanproviders', dest='foremanproviders', action='store_true', help='list foremanproviders')
    listinggroup.add_option('-l', '--profiles', dest='profiles', action='store_true', help='list available profiles')
    listinggroup.add_option('-S', '--storages', dest='storages', action='store_true', help='list available storage')
    listinggroup.add_option('-v', '--virtualproviders', dest='virtualproviders', action='store_true', help='list virtual providers')
    listinggroup.add_option('-Q', '--physicalproviders', dest='physicalproviders', action='store_true', help='list physical providers')
    listinggroup.add_option('-V', '--vms', dest='vms', action='store_true', help='list all vms')
    listinggroup.add_option("-Z", "--virtualprovider", dest="virtualprovider", type="string", help="Specify virtualprovider")
    parser.add_option_group(listinggroup)
    stackgroup = optparse.OptionGroup(parser, "Stack options")
    stackgroup.add_option("-q", "--stack", dest="stack",type="string", help="specify Stack")
    stackgroup.add_option('-X', '--stacks', dest='stacks', action='store_true', help='list all stacks')
    stackgroup.add_option('-5', '--startstack', dest="startstack", action='store_true', help='start stack. Requires you to use -q to indicate a stack')
    stackgroup.add_option('-6', '--stopstack', dest='stopstack', action='store_true', help='stop stack. Requires you to use -q to indicate a stack')
    stackgroup.add_option('-7', '--showstack', dest='showstack', action='store_true', help='show stack. Requires you to use -q to indicate a stack')
    stackgroup.add_option('-8', '--killstack', dest='killstack', action='store_true', help='kill stack. Requires you to use -q to indicate a stack')
    parser.add_option_group(stackgroup)
    parser.add_option("-C", "--client", dest="client", type="string", help="Specify Client")
    parser.add_option("-9", "--switchclient", dest="switchclient", type="string", help="Switch default client")
    (options, args) = parser.parse_args()
    client = options.client
    profile = options.profile
    profiles = options.profiles
    listclients = options.listclients
    storages = options.storages
    vms = options.vms
    stack = options.stack
    stacks = options.stacks
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
    storage = options.storage
    startstack = options.startstack
    stopstack = options.stopstack
    showstack = options.showstack
    killstack = options.killstack
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
            print "name: %s provider: %s" % ( storage['name'], storage['provider'].replace("/nuages/api/v1/virtualprovider/",'') )
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
        results = n.vms()
        allvms = []
        for vm in results:
            allvms.append(vm['name'])
        for vm in sorted(allvms):
            print vm
        sys.exit(0)
    if stacks:
        results = n.stacks()
        allstacks = []
        for stack in results:
            allstacks.append(stack['name'])
        for stack in sorted(allstacks):
            print stack
        sys.exit(0)
    if profile and not create:
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
    if stack:
        stacks = []
        for sta in sorted(n.stacks(), key=lambda stack: stack['name']):
            stacks.append(sta['name'])
        if not stack in stacks:
            print "Stack %s not found" % stack
            sys.exit(0)
        results = n.stack(stack)
        for attribute in sorted(results):
            if attribute in ['resource_uri'] or results[attribute]=='' or results[attribute]==None:
                continue
            print "%s: %s" % (attribute, str(results[attribute]).replace("/nuages/api/v1/%s/" % attribute,''))
        if startstack:
            results = n.startstack(stack)
            print "Stack %s started" % stack
            sys.exit(0)
        if stopstack:
            results = n.stopstack(stack)
            print "Stack %s stopped" % stack
            sys.exit(0)
        if showstack:
            results = n.showstack(stack)
            baseurl = "http://%s:%s" % (host, port)
            print results
            sys.exit(0)
        if killstack:
            n.killstack(stack)
            n.deletestack(stack)
            print "Stack %s killed" % stack
            sys.exit(0)
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
    if start:
        name = checkargs(args)
        n.start(name)
        print "VM %s started" % name
    if stop:
        name = checkargs(args)
        n.stop(name)
        print "VM %s stopped" % name
        sys.exit(0)
    if delete:
        name = checkargs(args)
        n.delete(name)
        print "VM %s deleted" % name
        sys.exit(0)
    if kill:
        name = checkargs(args)
        n.kill(name)
        n.delete(name)
        print "VM %s killed" % name
        sys.exit(0)
    if console:
        name = checkargs(args)
        results = n.console(name)
        baseurl = "http://%s:%s" % (host, port)
        print "%s%s" % (baseurl, results)
        sys.exit(0)
    if create and profile:
        name = None
        if len(args) == 1:
            name = args[0]
        profiles = []
        for prof in sorted(n.profiles(), key=lambda profile: profile['name']):
            profiles.append(prof['name'])
        if not profile in profiles:
            print "Profile %s not found" % profile
            sys.exit(0)
        details = n.profile(profile)
        if not details['autostorage'] and not storage:
            print "This profile requires a storagedomain to be set"
            sys.exit(0)
        if details['autostorage'] and storage:
            print "This profile will calculate the best storagedomain"
        if not details['ipamprovider'] and not name:
            print "This profile requires a name to be set"
            sys.exit(0)
        results = n.create(profile=profile, name=name, storage=storage, ip1=ip1, ip2=ip2, ip3=ip3, ip4=ip4, hostgroup=hostgroup, iso=iso, parameters=parameters, puppetclasses=puppetclasses)
        if name:
            print "VM %s created" % name
        else:
            lastvm = sorted(n.vms(),key=lambda vm: int(vm['id']))[-1]
            print "VM %s created" % lastvm['name']
    if len(args) == 1:
        name =  args[0]
        results = n.vm(name)
        for attribute in sorted(results):
            if attribute in ['create','iso','resource_uri','status'] or results[attribute]=='' or results[attribute]==None:
                continue
            print "%s: %s" % (attribute, str(results[attribute]).replace("/nuages/api/v1/%s/" % attribute,''))
        print "status: %s" % n.status(name)
