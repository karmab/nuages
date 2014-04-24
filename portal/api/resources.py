from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from portal.models import *

class CreatedByResource(ModelResource):
    class Meta:
        queryset        = User.objects.all()
        resource_name   = 'createdby'
        allowed_methods = ['get']
        excludes        = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authentication = BasicAuthentication()

class PhysicalProviderResource(ModelResource):
    class Meta:
        queryset        = PhysicalProvider.objects.all()
        resource_name   = 'physicalprovider'
        allowed_methods = ['get']
        fields          = ['name']
        authentication = BasicAuthentication()

class VirtualProviderResource(ModelResource):
    class Meta:
        queryset        = VirtualProvider.objects.all()
        resource_name   = 'virtualprovider'
        allowed_methods = ['get']
        fields          = ['name','type']
        authentication = BasicAuthentication()

class ForemanProviderResource(ModelResource):
    class Meta:
        queryset        = ForemanProvider.objects.all()
        resource_name   = 'foremanprovider'
        allowed_methods = ['get']
        fields          = ['name']
        authentication = BasicAuthentication()

class CobblerProviderResource(ModelResource):
    class Meta:
        queryset        = CobblerProvider.objects.all()
        resource_name   =  'cobblerprovider'
        allowed_methods = ['get']
        fields = ['name']
        authentication = BasicAuthentication()

class ProfileResource(ModelResource):
    physicalprovider = fields.ForeignKey(PhysicalProviderResource, 'physicalprovider', null=True, blank=True)
    virtualprovider  = fields.ForeignKey(VirtualProviderResource, 'virtualprovider', null=True, blank=True)
    foremanprovider  = fields.ForeignKey(ForemanProviderResource, 'foremanprovider', null=True, blank=True)
    cobblerprovider  = fields.ForeignKey(CobblerProviderResource, 'cobblerprovider', null=True, blank=True)
    class Meta:
        queryset       = Profile.objects.all()
        resource_name  = 'profile'
        authentication = BasicAuthentication()
        authorization  = DjangoAuthorization()

class VMResource(ModelResource):
    createdby        = fields.ForeignKey(CreatedByResource, 'createdby')
    class Meta:
        queryset       =  VM.objects.all()
        authentication = BasicAuthentication()
        authorization  = DjangoAuthorization()

class StackResource(ModelResource):
    createdby        = fields.ForeignKey(CreatedByResource, 'createdby')
    class Meta:
        queryset       =  Stack.objects.all()
        authentication = BasicAuthentication()
        authorization  = DjangoAuthorization()
