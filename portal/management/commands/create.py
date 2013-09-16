from django.core.management.base import BaseCommand, CommandError
from portal.models import *

class Command(BaseCommand):
	args = 'name storagedomain profile username'
	help = 'Quickly create a vm'
	def handle(self, *args, **options):
		#name ,storagedomain , profile, createdby = "t4000", "images", "basic6", "karim"
		name ,storagedomain , profile, createdby = args[0], args[1], args[2], arg[3]
		physical, ip1, mac1, ip2, mac2, ip3, mac3, ip4, mac4, puppetclasses, parameters, iso, ipilo, hostgroup  = False, None, None, None, None, None, None, None, None, None, '', '', None, ''
		profile=Profile.objects.get(name=profile)
		clu,guestid,memory,numcpu,disksize1,diskformat1,disksize2,diskformat2,diskinterface,numinterfaces,net1,subnet1,net2,subnet2,net3,subnet3,net4,subnet4,netinterface,dns,foreman,cobbler,requireip=profile.clu,profile.guestid,profile.memory,profile.numcpu,profile.disksize1,profile.diskformat1,profile.disksize2,profile.diskformat2,profile.diskinterface,profile.numinterfaces,profile.net1,profile.subnet1,profile.net2,profile.subnet2,profile.net3,profile.subnet3,profile.net4,profile.subnet4,profile.netinterface,profile.dns,profile.foreman,profile.cobbler,profile.requireip
		virtualprovider, cobblerprovider, foremanprovider , physicalprovider = profile.virtualprovider, profile.cobblerprovider , profile.foremanprovider , profile.physicalprovider
		username = User.objects.get(username=createdby)
		newvm=VM(name=name,storagedomain=storagedomain,physicalprovider=physicalprovider,virtualprovider=virtualprovider,physical=physical,cobblerprovider=cobblerprovider,foremanprovider=foremanprovider,profile=profile,ip1=ip1,mac1=mac1,ip2=ip2,mac2=mac2,ip3=ip3,mac3=mac3,ip4=ip4,mac4=mac4,puppetclasses=puppetclasses,parameters=parameters,createdby=username,iso=iso,ipilo=ipilo,hostgroup=hostgroup)
		success = newvm.save()
		self.stdout.write("Result:%s creating this VM" % success )
