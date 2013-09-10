from django.contrib import admin
from portal.models import *
from portal.adminforms import *

class IpamProviderAdmin(admin.ModelAdmin):
    form = IpamProviderForm

class PhysicalProviderAdmin(admin.ModelAdmin):
    form = PhysicalProviderForm

class LdapProviderAdmin(admin.ModelAdmin):
    form = LdapProviderForm

class VirtualProviderAdmin(admin.ModelAdmin):
    form = VirtualProviderForm

class ForemanProviderAdmin(admin.ModelAdmin):
    form = ForemanProviderForm

class CobblerProviderAdmin(admin.ModelAdmin):
    form = CobblerProviderForm

admin.site.register(VirtualProvider,VirtualProviderAdmin)
admin.site.register(PhysicalProvider,PhysicalProviderAdmin)
admin.site.register(CobblerProvider,CobblerProviderAdmin)
admin.site.register(ForemanProvider,ForemanProviderAdmin)
admin.site.register(Profile)
admin.site.register(Storage)
admin.site.register(VM)
admin.site.register(Default)
admin.site.register(LdapProvider,LdapProviderAdmin)
admin.site.register(IpamProvider,IpamProviderAdmin)
