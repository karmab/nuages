import paramiko

def checkstatus(stdout):
    for line in stdout:
        if 'status' in line:
            result=line.split('=')[1].replace('\r\n','')
            return int(result)
    return 1



class Ilo:
    def __init__(self,host,username,password):
        self.host,self.username,self.password = host,username,password

    def getmacs(self):
        host, username, password = self.host, self.username, self.password
        macs=[]
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('show system1/network1/Integrated_NICs')
        for line in stdout:
            if 'NIC_MACAddress' in line:
            #macs.append(line.split('=')[1].replace('\r\n',''))
                macs.append(line.split('=')[0].replace(' ','')+"="+line.split('=')[1].replace('\r\n',''))
        s.close()
        return macs

    def reset(self):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('power reset')
        s.close()
        return 0

    def pxe(self):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('set /system1/bootconfig1/bootsource5 bootorder=1')
        s.close()
        return 0

    def start(self):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('power on')
        s.close()
        return 0

    def status(self):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('power')
        s.close()
        if 'On' in stdout:
            return 'down'
        else:
            return 'up'

    def stop(self):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command('power off')
        s.close()
        return 0

    def iso(self,isourl):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command("vm cdrom insert %s" % isourl )
        s.close()
        return 0

    def bootonce(self):
        host, username, password = self.host, self.username, self.password
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(host, username=username, password=password)
        stdin, stdout, stderr = s.exec_command("vm cdrom set boot_once" )
        s.close()
        return 0
