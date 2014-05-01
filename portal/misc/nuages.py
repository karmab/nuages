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
    def createvm(self,name,profile):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm" % (protocol, host, port)
        data = { "profile" : profile , "name" : name }
        r = requests.post(url,verify=False, data=json.dumps(data), headers=headers, auth=(user,password))
        print r , r.reason, r.text
        #results = r.json()['results']
        #return results
    def allvms(self):
        allvms = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for vm in results:
            allvms.append(vm['name'])
        return allvms
    def profiles(self):
        profiles = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/profile" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for profile in results:
            profiles.append(profile['name'])
        return profiles
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
    def deletevm(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s" % (protocol, host, port, name)
        r = requests.delete(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def killvm(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/kill" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def startvm(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/start" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def stopvm(self,name):
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/vm/%s/stop" % (protocol, host, port, name)
        r = requests.post(url,verify=False, headers=headers,auth=(user,password))
        return r.text.replace('"','')
    def virtualproviders(self):
        vps = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/virtualprovider" % (protocol, host, port)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for vp in results:
            vps.append(vp['name'])
        return vps

if __name__ == '__main__':
    usage = 'wrapper around nuages api'
    version = '1.1'
    parser = optparse.OptionParser('Usage: %prog [options] vmname',version=version)
    actiongroup = optparse.OptionGroup(parser, 'Action options')
    actiongroup.add_option('-o', '--console', dest='console', action='store_true', help='get console')
    actiongroup.add_option('-s', '--startvm', dest='startvm', action='store_true', help='start vm')
    actiongroup.add_option('-w', '--stopvm', dest='stopvm', action='store_true', help='stop vm')
    parser.add_option_group(actiongroup)
    creationgroup = optparse.OptionGroup(parser, 'Creation options')
    creationgroup.add_option('-d', '--deletevm', dest='deletevm', action='store_true', help='delete vm')
    creationgroup.add_option('-k', '--killvm', dest='killvm', action='store_true', help='kill vm')
    creationgroup.add_option("-p", "--profile", dest="profile",type="string", help="specify Profile")
    creationgroup.add_option('-n', '--createvm', dest='createvm', action='store_true', help='create vm')
    parser.add_option_group(creationgroup)
    listinggroup = optparse.OptionGroup(parser, "Creation options")
    listinggroup.add_option('-L', '--listclients', dest="listclients", action='store_true', help='list available clients')
    listinggroup.add_option('-c', '--cobblerproviders', dest='cobblerproviders', action='store_true', help='list cobblerproviders')
    listinggroup.add_option('-f', '--foremanproviders', dest='foremanproviders', action='store_true', help='list foremanproviders')
    listinggroup.add_option('-l', '--listprofiles', dest='listprofiles', action='store_true', help='list available profiles')
    listinggroup.add_option('-v', '--virtualproviders', dest='virtualproviders', action='store_true', help='list virtual providers')
    listinggroup.add_option('-Q', '--physicalproviders', dest='physicalproviders', action='store_true', help='list physical providers')
    listinggroup.add_option('-V', '--listvms', dest='listvms', action='store_true', help='list all vms')
    parser.add_option_group(listinggroup)
    parser.add_option("-C", "--client", dest="client", type="string", help="Specify Client")
    parser.add_option("-9", "--switchclient", dest="switchclient", type="string", help="Switch default client")
    (options, args) = parser.parse_args()
    client = options.client
    profile = options.profile
    listprofiles = options.listprofiles
    listclients = options.listclients
    listvms = options.listvms
    cobblerproviders = options.cobblerproviders
    foremanproviders = options.foremanproviders
    physicalproviders = options.physicalproviders
    virtualproviders = options.virtualproviders
    switchclient = options.switchclient
    console = options.console
    startvm = options.startvm
    createvm = options.createvm
    killvm = options.killvm
    deletevm = options.deletevm
    stopvm = options.stopvm
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
    if listprofiles:
        for profile in sorted(n.profiles()):
            print profile
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
    if listvms:
        for vm in sorted(n.allvms()):
            print vm
        sys.exit(0)
    if len(args) != 1:
        print 'Name required'
        sys.exit(0)
    name = args[0]
    if startvm:
        results = n.startvm(name)
        print results
    if stopvm:
        results = n.stopvm(name)
        print results
    if deletevm:
        results = n.deletevm(name)
        print results
    if killvm:
        results = n.killvm(name)
        print results
    if console:
        results = n.console(name)
        baseurl = "http://%s:%s" % (host, port)
        print "%s%s" % (baseurl, results)
    if createvm and profile:
        results = n.createvm(name,profile)
        print results
