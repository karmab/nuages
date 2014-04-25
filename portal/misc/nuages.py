import json
import requests
import simplejson 

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
    def profiles(self):
        profiles = []
        host, port, user , password, protocol, headers = self.host, self.port, self.user, self.password, self.protocol, self.headers
        url = "%s://%s:%s/nuages/api/v1/profile" % (protocol, host, port)
        url = "%s://%s/nuages/api/v1/profile" % (protocol, host)
        r = requests.get(url,verify=False, headers=headers,auth=(user,password))
        results = r.json()['results']
        for profile in results:
            profiles.append(profile['name'])
        return profiles

n  = Nuage('192.168.8.6',80,'admin','prout')
print n.profiles()
