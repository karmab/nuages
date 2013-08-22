from django.contrib import admin
from portal.models import *

admin.site.register(VirtualProvider)
admin.site.register(PhysicalProvider)
admin.site.register(CobblerProvider)
admin.site.register(ForemanProvider)
admin.site.register(Profile)
admin.site.register(Storage)
admin.site.register(VM)
admin.site.register(Default)
admin.site.register(LdapProvider)
