from django.contrib import admin
from portal.models import VirtualProvider,PhysicalProvider,CobblerProvider,ForemanProvider,Type,Profile,VM,Storage,Default,LdapProvider

admin.site.register(VirtualProvider)
admin.site.register(PhysicalProvider)
admin.site.register(CobblerProvider)
admin.site.register(ForemanProvider)
admin.site.register(Type)
admin.site.register(Profile)
admin.site.register(Storage)
admin.site.register(VM)
admin.site.register(Default)
admin.site.register(LdapProvider)
