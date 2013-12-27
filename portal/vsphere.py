#!/usr/bin/env jython

import random
import os
from com.vmware.vim25 import *
from com.vmware.vim25.mo import *
import java.net.URL as URL
import sys


#0-define auxiliary functions
def convert(octets):
    return str(float(octets)/1024/1024/1024)+"GB"

def dssize(ds):
    di = ds.getSummary()
    return convert(di.getCapacity()), convert(di.getFreeSpace())

def makecuspec(si, ori, dest, ip):
    specmanager = si.getCustomizationSpecManager()
    specmanager.duplicateCustomizationSpec(ori,dest)
    newspec = specmanager.getCustomizationSpec(dest)
    info = newspec.getInfo()
    info.setName(dest)
    info.setDescription(dest)
    newspec.setInfo(info)
    specdetails = newspec.getSpec()
    custoname = CustomizationFixedName()
    custoname.setName(dest)
    specdetails.getIdentity().setHostName(custoname)
    adapter = specdetails.getNicSettingMap()[0].getAdapter()
    adapter.getIp().setIpAddress(ip)
    specmanager.overwriteCustomizationSpec(newspec)
    return specdetails


def createnicspec(nicname, netname, guestid):
    nicspec = VirtualDeviceConfigSpec()
    nicspec.setOperation(VirtualDeviceConfigSpecOperation.add)
    if guestid in ["rhel4guest","rhel4_64guest"]:
        #nic=VirtualPCNet32()
        nic = VirtualVmxnet()
    else:
        nic = VirtualVmxnet3()
    desc = Description()
    desc.setLabel(nicname)
    nicbacking = VirtualEthernetCardNetworkBackingInfo()
    desc.setSummary(netname)
    nicbacking.setDeviceName(netname)
    nic.setBacking(nicbacking)
    nic.setKey(0)
    nic.setDeviceInfo(desc)
    nic.setAddressType("generated")
    nicspec.setDevice(nic)
    return nicspec


def creatediskspecold(disksize,ds,diskmode,thin=False,ckey=1000):
    #SCSISPEC
    scsispec = VirtualDeviceConfigSpec()
    scsispec.setOperation(VirtualDeviceConfigSpecOperation.add)
    scsictrl = VirtualLsiLogicController()
    scsictrl.setKey(ckey)
    scsictrl.setBusNumber(0)
    scsictrl.setSharedBus(VirtualSCSISharing.noSharing)
    scsispec.setDevice(scsictrl)
    diskspec = VirtualDeviceConfigSpec()
    diskspec.setOperation(VirtualDeviceConfigSpecOperation.add)
    diskspec.setFileOperation(VirtualDeviceConfigSpecFileOperation.create)
    vd = VirtualDisk()
    vd.setCapacityInKB(disksize)
    diskspec.setDevice(vd)
    #vd.setKey(0)
    vd.setUnitNumber(0)
    vd.setControllerKey(ckey)
    diskfilebacking = VirtualDiskFlatVer2BackingInfo()
    filename = "["+ ds.getName() +"]"
    diskfilebacking.setFileName(filename)
    diskfilebacking.setDiskMode(diskmode)
    if thin:
        diskfilebacking.setThinProvisioned(True)
    else:
        diskfilebacking.setThinProvisioned(False)
    vd.setBacking(diskfilebacking)
    return scsispec, diskspec, filename

def createscsispec():
    ckey = 1000
    #SCSISPEC
    scsispec = VirtualDeviceConfigSpec()
    scsispec.setOperation(VirtualDeviceConfigSpecOperation.add)
    scsictrl = VirtualLsiLogicController()
    scsictrl.setKey(ckey)
    scsictrl.setBusNumber(0)
    scsictrl.setSharedBus(VirtualSCSISharing.noSharing)
    scsispec.setDevice(scsictrl)
    return scsispec

def creatediskspec(number, disksize, ds, diskmode, thin=False):
    ckey = 1000
    diskspec = VirtualDeviceConfigSpec()
    diskspec.setOperation(VirtualDeviceConfigSpecOperation.add)
    diskspec.setFileOperation(VirtualDeviceConfigSpecFileOperation.create)
    vd = VirtualDisk()
    vd.setCapacityInKB(disksize)
    diskspec.setDevice(vd)
    #vd.setKey(1)
    vd.setUnitNumber(number)
    vd.setControllerKey(ckey)
    diskfilebacking = VirtualDiskFlatVer2BackingInfo()
    filename = "["+ ds.getName() +"]"
    #filename = "[%s] %s/%s_%s.vmdk" % (ds.getName(),name,name,number)
    diskfilebacking.setFileName(filename)
    diskfilebacking.setDiskMode(diskmode)
    if thin:
        diskfilebacking.setThinProvisioned(True)
    else:
        diskfilebacking.setThinProvisioned(False)
    vd.setBacking(diskfilebacking)
    return diskspec


def createcdspec():
    #http://books.google.es/books?id=SdsnGmhF0QEC&pg=PA145&lpg=PA145&dq=VirtualCdrom%2Bspec&source=bl&ots=s8O2mw437-&sig=JpEo-AqmDV42b3fxpTcCt4xknEA&hl=es&sa=X&ei=KgGfT_DqApOy8QOl07X6Dg&redir_esc=y#v=onepage&q=VirtualCdrom%2Bspec&f=false
    cdspec = VirtualDeviceConfigSpec()
    cdspec.setOperation(VirtualDeviceConfigSpecOperation.add)
    cd=VirtualCdrom()
    cdbacking=VirtualCdromAtapiBackingInfo()
    sys.exit(0)
    cd.setBacking(cdbacking)
    cd.setControllerKey(201)
    cd.setUnitNumber(0)
    cd.setKey(-1)
    cdspec.setDevice(cd)
    return cdspec

def createisospec(iso=None):
    cdspec = VirtualDeviceConfigSpec()
    cdspec.setOperation(VirtualDeviceConfigSpecOperation.add)
    connect=VirtualDeviceConnectInfo()
    connect.setStartConnected(True)
    connect.setAllowGuestControl(True)
    connect.setConnected(False)
    cd=VirtualCdrom()
    cd.setConnectable(connect)
    cdbacking=VirtualCdromIsoBackingInfo()
    if iso:
        cdbacking.setFileName(iso)
    cd.setBacking(cdbacking)
    cd.setControllerKey(201)
    cd.setUnitNumber(0)
    cd.setKey(-1)
    cdspec.setDevice(cd)
    return cdspec


def createclonespec(pool):
    clonespec = VirtualMachineCloneSpec()
    relocatespec = VirtualMachineRelocateSpec()
    relocatespec.setPool(pool.getMOR())
    clonespec.setLocation(relocatespec)
    clonespec.setPowerOn(False)
    clonespec.setTemplate(False)
    return clonespec

def stopvm(vm):
    if vm.getRuntime().getPowerState().toString()=="poweredOn":
        t = vm.powerOffVM_Task()
        result = t.waitForMe()
        print "%s powering off VM"% (result)

def startvm(vm):
    if vm.getRuntime().getPowerState().toString()=="poweredOff":
        t = vm.powerOnVM_Task(None)
        result = t.waitForMe()
        print "%s powering on VM"% (result)

guestid532 = 'rhel5guest'
guestid564 = 'rhel5_64Guest'
guestid632 = 'rhel6guest'
guestid664 = 'rhel6_64Guest'
nicname1 = 'Network Adapter 1'
nicname2 = 'Network Adapter 2'
nicname3 = 'Network Adapter 3'
nicname4 = 'Network Adapter 4'
guests = { 'rhel_5': guestid532, 'rhel_5x64' : guestid564, 'rhel_6': guestid632 , 'rhel_6x64' : guestid664 }

class Vsphere:
    def __init__(self, vcip, vcuser, vcpassword, dc, clu):
        url = "https://"+vcip+"/sdk"
        #4-1-CONNECT
        si = ServiceInstance(URL(url), vcuser, vcpassword , True)
        self.si = si
        self.vcip = vcip
        self.rootFolder = si.getRootFolder()
        self.dc = InventoryNavigator(self.rootFolder).searchManagedEntity("Datacenter",dc)
        self.macaddr = []
        self.clu = clu

#       clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource",clu)
#       self.vmfolder = dc.getVmFolder()
#       hosts=InventoryNavigator(rootFolder).searchManagedEntities("HostSystem")
#       morhosts={}
#       hostlist={}
#       clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource",clu)
#       self.clu = clu
#       pool = clu.getResourcePool()
#       self.pool = pool
#       for h in hosts:
#               morhosts[h.getMOR()] = h.getName()
#               hostlist[h.getName()] = h
#       self.hostlist = hostlist
#       bestesx = {}
#       for hst in clu.getHosts():
#               if hst.getSummary().getRuntime().isInMaintenanceMode():
#                       continue
#               counter=0
#               for vm in hst.getVms():
#                       if vm.getRuntime().getPowerState().toString()=="poweredOn":
#                               counter = counter+1
#               bestesx[counter] = hst
#       host = bestesx[min(bestesx.keys())]
#       self.best = host


    def create(self, name, numcpu, numinterfaces, diskmode1,disksize1, ds, memory, guestid, net1, net2=None, net3=None, net4=None, thin=False,distributed=False,disksize2=None,diskmode2=None,vnc=False,iso=None):
        memory = int(memory)
        numcpu = int(numcpu)
        disksize1 = int(disksize1)
        if disksize2:
            disksize2 = int(disksize2)
        numinterfaces = int(numinterfaces)
        if guestid in guests.keys():
            guestid = guests[guestid]
        disksize1 = disksize1*1048576
        disksizeg1 = convert(1000*disksize1)
        if disksize2:
            disksize2 = disksize2*1048576
            disksizeg2 = convert(1000*disksize2)
        dclist = {}
        dslist = {}
        networklist = {}
        guestlist = []
        #si = self.si
        rootFolder = self.rootFolder
        dc = self.dc
        vmfolder = dc.getVmFolder()
        clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource",self.clu)
        pool = clu.getResourcePool()

        #SELECT DS
        datastore = InventoryNavigator(rootFolder).searchManagedEntity("Datastore",ds)
        if not datastore:
            return "%s not found,aborting" % (ds)
        #TODO:change this if to a test sum of all possible disks to be added to this datastore
        if float(dssize(datastore)[1].replace("GB","")) -float(disksizeg1.replace("GB","")) <= 0:
            return "New Disk too large to fit in selected Datastore,aborting..."
        #define specifications for the VM
        confspec = VirtualMachineConfigSpec()
        confspec.setName(name)
        confspec.setAnnotation(name)
        confspec.setMemoryMB(memory)
        confspec.setNumCPUs(numcpu)
        confspec.setGuestId(guestid)
        if vnc:
            #enable VNC
            vncport = random.randint(5900, 7000)
            opt1 = OptionValue()
            opt1.setKey('RemoteDisplay.vnc.port')
            opt1.setValue(vncport);
            opt2 = OptionValue()
            opt2.setKey('RemoteDisplay.vnc.enabled')
            opt2.setValue("TRUE");
            confspec.setExtraConfig([opt1,opt2])

        #scsispec1, diskspec1, filename1 = creatediskspec(disksize1, datastore, diskmode1, thin)
        scsispec1 = createscsispec()
        diskspec1 = creatediskspec(0, disksize1, datastore, diskmode1, thin)
        devconfspec = [scsispec1, diskspec1]

        if disksize2:
            diskspec2 = creatediskspec(1, disksize2, datastore, diskmode2, thin)
            devconfspec.append(diskspec2)

        #NICSPEC
        if numinterfaces >= 1:
            #NIC 1
            nicspec1 = createnicspec(nicname1, net1, guestid)
        if numinterfaces >= 2:
            #NIC 2
            nicspec2 = createnicspec(nicname2, net2, guestid)
        if numinterfaces >= 3:
            #NIC 3
            nicspec3 = createnicspec(nicname3, net3, guestid)
        if numinterfaces >= 4:
            #NIC 4
            nicspec4 = createnicspec(nicname4, net4, guestid)

        if numinterfaces ==1:
            devconfspec.append(nicspec1)
        if numinterfaces ==2:
            devconfspec.append(nicspec2)
        if numinterfaces ==3:
            devconfspec.append(nicspec3)
        if numinterfaces ==4:
            devconfspec.append(nicspec4)

        if iso:
            #add iso
            cdspec=createisospec(iso)
            devconfspec.append(cdspec)

        confspec.setDeviceChange(devconfspec)

        confspec.setDeviceChange(devconfspec)
        vmfi = VirtualMachineFileInfo()
        filename = "["+ ds +"]"
        vmfi.setVmPathName(filename)
        confspec.setFiles(vmfi)

        t = vmfolder.createVM_Task(confspec,pool,None)
        result = t.waitForMe()
        #print "%s on creation of %s" % (result,name)

        #2-GETMAC
        vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine",name)
        if not vm:
            return "%s not found" % (name)
        devices = vm.getConfig().getHardware().getDevice()
        macaddr = []
        for dev in devices:
            if "addressType" in dir(dev):
                macaddr.append(dev.getMacAddress())
        self.macaddr = macaddr
        #HANDLE DVS
        if distributed:
            portgs = {}
            dvnetworks = InventoryNavigator(rootFolder).searchManagedEntities("DistributedVirtualSwitch")
            for dvnetw in dvnetworks:
                uuid = dvnetw.getUuid()
                for portg in dvnetw.getPortgroup():
                    portgs[portg.getName()] = [uuid,portg.getKey()]
            for k in range(len(nets)):
                net = nets[k]
                mactochange = macaddr[k]
                if net in portgs.keys():
                    confspec = VirtualMachineConfigSpec()
                    nicspec = VirtualDeviceConfigSpec()
                    nicspec.setOperation(VirtualDeviceConfigSpecOperation.edit)
                    nic = VirtualPCNet32()
                    dnicbacking = VirtualEthernetCardDistributedVirtualPortBackingInfo()
                    dvconnection = DistributedVirtualSwitchPortConnection()
                    dvconnection.setSwitchUuid(portgs[net][0])
                    dvconnection.setPortgroupKey(portgs[net][1])
                    dnicbacking.setPort(dvconnection)
                    nic.setBacking(dnicbacking)
                    nicspec.setDevice(nic)
                    #2-GETMAC
                    vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
                    if not vm:
                        return "%s not found" % (name)
                    devices = vm.getConfig().getHardware().getDevice()
                    for dev in devices:
                        if "addressType" in dir(dev):
                            mac = dev.getMacAddress()
                            if mac==mactochange:
                                dev.setBacking(dnicbacking)
                                nicspec.setDevice(dev)
                                devconfspec=[nicspec]
                                confspec.setDeviceChange(devconfspec)
                                t = vm.reconfigVM_Task(confspec)
                                result = t.waitForMe()
                                #print "%s for changing DistributedVirtualSwitch for mac %s of %s" % (result, mac, name)
        self.macaddr = macaddr
        return macaddr


    def getmacs(self,name):
        rootFolder = self.rootFolder
        vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine",name)
        if not vm:
            return None
        devices = vm.getConfig().getHardware().getDevice()
        macs = []
        for dev in devices:
            if "addressType" in dir(dev):
                netname=dev.getBacking().getDeviceName()
                macaddress = dev.getMacAddress()
                macs.append("%s=%s" % (netname,macaddress))
        return macs

    def start(self, name):
        rootFolder = self.rootFolder
        vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
        if not vm:
            return "%s not found" % (name)
        if vm.getRuntime().getPowerState().toString()=="poweredOff":
            t = vm.powerOnVM_Task(None)
            result = t.waitForMe()
            return "%s started"% (name)

    def remove(self, name):
        rootFolder = self.rootFolder
        vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
        if not vm:
            return "%s not deleted"% (name)
        if vm.getRuntime().getPowerState().toString()=="poweredOn":
            t = vm.powerOffVM_Task()
            result = t.waitForMe()
        t = vm.destroy_Task()
        result = t.waitForMe()
        return "%s deleted"% (name)

    def stop(self, name):
        rootFolder = self.rootFolder
        vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
        if not vm:
            return "%s not found,aborting" % (name)
        if vm.getRuntime().getPowerState().toString()=="poweredOn":
            t = vm.powerOffVM_Task()
            result = t.waitForMe()
            return "%s stopped"% (name)

    def status(self, name):
        rootFolder = self.rootFolder
        vm = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
        if not vm:
            #print "%s not found,aborting" % (name)
            return ''
        else:
            return vm.getRuntime().getPowerState().toString()

    def console(self, name):
        rootFolder = self.rootFolder
        vm=InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
        if not vm or vm.getRuntime().getPowerState().toString()=="poweredOff":
            return None,None
        extraconfig = vm.getConfig().getExtraConfig()
        vncfound = False
        for extra in extraconfig:
            key, value = extra.getKey(), extra.getValue()
            if 'vnc' in key:
                vncfound = True
                vncport = value
                break
            else:
                continue
        if vncfound:
            morhosts={}
            hosts=InventoryNavigator(rootFolder).searchManagedEntities("HostSystem")
            for h in hosts:
                morhosts[h.getMOR()]=h.getName()
            morhost = vm.getRuntime().getHost()
            host = morhosts[morhost]
            return host,vncport
        else:
            return None,None

    def html5console(self, name, fqdn, sha1):
        vcip = self.vcip
        vcconsoleport = "7331"
        si = self.si
        rootFolder = self.rootFolder
        vm=InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", name)
        if not vm:
            return "%s not found,aborting" % (name)
        sessionmanager = si.getSessionManager()
        session = sessionmanager.acquireCloneTicket()
        vmid = vm.getMOR().get_value()
        vmurl = "http://%s:%s/console/?vmId=%s&vmName=%s&host=%s&sessionTicket=%s&thumbprint=%s" % (vcip, vcconsoleport, vmid, name, fqdn, session, sha1)
        return vmurl

    def allvms(self):
        translation = {'poweredOff':'down', 'poweredOn':'up'}
        rootFolder = self.rootFolder
        vms = {}
        vmlist= InventoryNavigator(rootFolder).searchManagedEntities("VirtualMachine")
        for vm in vmlist:
            vms[vm.getName()] = translation[vm.getRuntime().getPowerState().toString()]
        return vms

    def getstorage(self):
        dclist = {}
        hostlist = {}
        dslist = {}
        clusterlist = {}
        networklist = {}
        guestlist = []
        rootFolder = self.rootFolder
        dc = self.dc
        clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource",self.clu)
        results = {}
        for dts in clu.getDatastores():
            datastorename = dts.getName()
            total = dssize(dts)[0].replace('GB','')
            available = dssize(dts)[1].replace('GB','')
            results[datastorename] = [float(total), float(available), dc.getName()]
        return results


    def beststorage(self):
        dclist = {}
        hostlist = {}
        dslist = {}
        clusterlist = {}
        networklist = {}
        guestlist = []
        rootFolder = self.rootFolder
        dc = self.dc
        clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource",self.clu)
        bestds = ''
        bestsize = 0
        for dts in clu.getDatastores():
            datastorename = dts.getName()
            available = float(dssize(dts)[1].replace('GB',''))
            if available > bestsize:
                bestsize = available
                bestds = datastorename
        return bestds

    def getisos(self):
        rootFolder = self.rootFolder
        dc = self.dc
        clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource",self.clu)
        isos=[]
        results = {}
        searchspec = HostDatastoreBrowserSearchSpec()
        filequery = [IsoImageFileQuery(),FolderFileQuery()]
        filequeryflags = FileQueryFlags()
        filequeryflags.setFileSize(True)
        filequeryflags.setModification(False)
        filequeryflags.setFileOwner(False)
        filequeryflags.setFileType(False)
        searchspec.setQuery(filequery)
        searchspec.setDetails(filequeryflags)
        searchspec.setSortFoldersFirst(True)
        searchspec.setSearchCaseInsensitive(True)
        for dts in clu.getDatastores():
            datastorename = dts.getName()
            datastorepath = "["+ datastorename +"]"
            browser = dts.getBrowser()
            t  = browser.searchDatastore_Task(datastorepath, searchspec)
            t.waitForMe()
            result = t.getTaskInfo().getResult();
            fileinfo = result.getFile()
            for element in fileinfo:
                folderpath = element.getPath()
                if not folderpath.endswith('iso') and 'ISO' in folderpath.upper() :
                    t  = browser.searchDatastoreSubFolders_Task( "%s%s" % ( datastorepath, folderpath), searchspec)
                    t.waitForMe()
                    result = t.getTaskInfo().getResult();
                    results = result.getHostDatastoreBrowserSearchResults()
                    for r in results:
                        fileinfo = r.getFile()
                        for isofile in fileinfo:
                            path = isofile.getPath()
                            if path.endswith('.iso'):
                                isos.append("%s/%s/%s" % (datastorepath, folderpath, path))
        return isos


    def gettemplates(self):
        templates =  []
        rootFolder = self.rootFolder
        vms = InventoryNavigator(rootFolder).searchManagedEntities("VirtualMachine")
        for vm in vms:
            if vm.getConfig().isTemplate():
                templates.append(vm.getName())
        return templates

    def createfromtemplate(self, name, template):
        rootFolder = self.rootFolder
        template = InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", template)
        clu = InventoryNavigator(rootFolder).searchManagedEntity("ComputeResource", self.clu)
        pool = clu.getResourcePool()
        clonespec = createclonespec(pool)
        t = template.cloneVM_Task(template.getParent(),name,clonespec)
        result=t.waitForMe()
        return "%s on deploying %s from template" %(result, name)

if __name__ == '__main__':
    action, vcip, vcuser, vcpassword, dc, clu = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    vsphere = Vsphere(vcip, vcuser, vcpassword, dc, clu)
    if action == 'getstorage':
        print vsphere.getstorage()
    if action == 'beststorage':
        print vsphere.beststorage()
    if action == 'allvms':
        print vsphere.allvms()
    if action == 'getisos':
        print vsphere.getisos()
    elif action == 'start':
        name = sys.argv[7]
        print vsphere.start(name)
    elif action == 'stop':
        name = sys.argv[7]
        print vsphere.stop(name)
    elif action == 'status':
        name = sys.argv[7]
        print vsphere.status(name)
    elif action == 'remove':
        name = sys.argv[7]
        print vsphere.remove(name)
    elif action == 'getmacs':
        name = sys.argv[7]
        print vsphere.getmacs(name)
    elif action == 'html5console':
        name, fqdn, sha1 = sys.argv[7], sys.argv[8], sys.argv[9]
        print vsphere.hmtl5console(name, fqdn, sha1)
    elif action == 'console':
        name = sys.argv[7]
        print vsphere.console(name)
    elif action == 'gettemplates':
        print vsphere.gettemplates()
    elif action == 'createfromtemplate':
        name = sys.argv[7]
        template = sys.argv[8]
        print vsphere.createfromtemplate(name,template)
    elif action == 'create':
        net1, net2, net3, net4 = None, None, None, None
        name, numcpu, numinterfaces, disksize1, diskmode1, disksize2 , diskmode2, ds, memory, guestid, vnc, iso, net1 = sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12], sys.argv[13], sys.argv[14], sys.argv[15], sys.argv[16], sys.argv[17], sys.argv[18], sys.argv[19]
        diskmode1, diskmode2 = 'persistent', 'persistent'
        numcpu, numinterfaces, disksize1 = int(numcpu), int(numinterfaces), int(disksize1)
        if numinterfaces >= 2:
            net2 = sys.argv[20]
        if numinterfaces >= 3:
            net3 = sys.argv[21]
        if numinterfaces >= 4:
            net4 = sys.argv[22]
        if 'rue' in vnc or 'RUE' in vnc:
            vnc = True
        else:
            vnc = False
        if iso == '' or iso =='None':
            iso  = None
        if disksize2 == '' or disksize2 =='None':
            disksize2  = None
        if diskmode2 == '' or diskmode2 =='None':
            diskmode2  = None
        print vsphere.create(name=name, numcpu=numcpu, numinterfaces=numinterfaces, diskmode1=diskmode1, disksize1=disksize1, diskmode2=diskmode2, disksize2=disksize2, ds=ds, memory=memory, guestid=guestid, vnc=vnc, iso=iso, net1=net1, net2=net2, net3=net3,net4=net4)
