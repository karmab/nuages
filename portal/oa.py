import paramiko
import re

class Oa:
    def __init__(self,host,username,password):
        self.host,self.username,self.password = host,username,password

    def getid(self,name):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('show server list')
	id=None
        for line in stdout:
            if  name in line:
		matchid = re.search('([0-9]*) %s.*'% name , line)
		id = matchid.group(1)
		break
        s.close()
        return id

    def getmacs(self,bladeid):
        host, username, password = self.host, self.username, self.password
        macs=[]
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('show server info %s' % bladeid)
        for line in stdout:
            if 'Ethernet'  in line and 'NIC' in line:
		matchmac=re.search('.*\((NIC.*)\).* (..:..:..:..:..:..).*',line)
		macs.append("%s=%s" % ( matchmac.group(1), matchmac.group(2) ))
        s.close()
        return macs

    def reset(self,bladeid):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('reboot server %s force' % bladeid )
        s.close()
        return 0

    def pxe(self,bladeid):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('reboot server %s force pxe' % bladeid )
        s.close()
        return 0

    def start(self,bladeid):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('poweron server %s' % bladeid)
        s.close()
        return 0

    def startpxe(self,bladeid):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('poweron server %s pxe' % bladeid)
        s.close()
        return 0

    def status(self,bladeid):
	status='N/A'
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('show server status %s' % bladeid)
        for line in stdout:
            if 'Power:'  in line:	
		matchstatus = re.search('Power: (.*)',line)
		status = matchstatus.group(1)
        s.close()
	if status == 'On':
		return 'up'
	elif status =='Off':
        	return 'down'
	else:
        	return 'N/A'

    def stop(self,bladeid):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('poweroff server %s' % bladeid)
        s.close()
        return 0

#    def iso(self,isourl,bladeid):
#        host, username, password = self.host, self.username, self.password
#        s = paramiko.SSHClient()
#        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#        s.connect(host, username=username, password=password)
#        stdin, stdout, stderr = s.exec_command("vm cdrom insert %s" % isourl )
#        s.close()
#        return 0
#
#    def bootonce(self,bladeid):
#        host, username, password = self.host, self.username, self.password
#        s = paramiko.SSHClient()
#        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#        s.connect(host, username=username, password=password)
#        stdin, stdout, stderr = s.exec_command("vm cdrom set boot_once" )
#        s.close()
#        return 0
