from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from portal.models import *
from django.conf.urls import url
from django.db.models import Q
from customauthentication import StaffAuthentication
##from customauthorization import StaffAuthorization

def groupquery(user):
    usergroups  = user.groups
    query       = Q(createdby=user)
    allusers    = User.objects.all()
    for g in usergroups.all():
        for u in allusers:
            if u.username == user.username:
                continue
            if g in u.groups.all():
                query=query|Q(createdby=u)
    return query

class CreatedByResource(ModelResource):
    class Meta:
        queryset        = User.objects.all()
        resource_name   = 'createdby'
        allowed_methods = ['get']
        excludes        = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        authentication = BasicAuthentication()
        detail_uri_name = 'username'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class PhysicalProviderResource(ModelResource):
    class Meta:
        queryset        = PhysicalProvider.objects.all()
        resource_name   = 'physicalprovider'
        allowed_methods = ['get']
        fields          = ['name']
        authentication = BasicAuthentication()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class StorageResource(ModelResource):
    class Meta:
        queryset        = Storage.objects.all()
        resource_name   = 'storage'
        allowed_methods = ['get']
        #fields          = ['name']
        authentication = BasicAuthentication()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class VirtualProviderResource(ModelResource):
    class Meta:
        queryset        = VirtualProvider.objects.all()
        resource_name   = 'virtualprovider'
        allowed_methods = ['get']
        fields          = ['name','type']
        authentication = BasicAuthentication()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/storage$" % self._meta.resource_name, self.wrap_view('storage'), name="api_vm_start"),
        ]
    def storage(self, request, **kwargs):
         basic_bundle = self.build_bundle(request=request)
         virtualprovider = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
         return self.create_response(request, virtualprovider.storage())

class ForemanProviderResource(ModelResource):
    class Meta:
        queryset        = ForemanProvider.objects.all()
        resource_name   = 'foremanprovider'
        allowed_methods = ['get']
        fields          = ['name']
        authentication = BasicAuthentication()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class CobblerProviderResource(ModelResource):
    class Meta:
        queryset        = CobblerProvider.objects.all()
        resource_name   =  'cobblerprovider'
        allowed_methods = ['get']
        fields = ['name']
        authentication = BasicAuthentication()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class ProfileResource(ModelResource):
    physicalprovider = fields.ForeignKey(PhysicalProviderResource, 'physicalprovider', null=True, blank=True)
    virtualprovider  = fields.ForeignKey(VirtualProviderResource, 'virtualprovider', null=True, blank=True)
    foremanprovider  = fields.ForeignKey(ForemanProviderResource, 'foremanprovider', null=True, blank=True)
    cobblerprovider  = fields.ForeignKey(CobblerProviderResource, 'cobblerprovider', null=True, blank=True)
    class Meta:
        queryset       = Profile.objects.all()
        resource_name  = 'profile'
        authentication = StaffAuthentication()
        authorization  = DjangoAuthorization()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

class VMResource(ModelResource):
    createdby        = fields.ForeignKey(CreatedByResource, 'createdby')
    profile          = fields.ForeignKey(ProfileResource, 'profile')
    class Meta:
        queryset       =  VM.objects.all()
        authentication = StaffAuthentication()
        authorization  = DjangoAuthorization()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/console$" % self._meta.resource_name, self.wrap_view('console'), name="api_vm_console"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/kill$" % self._meta.resource_name, self.wrap_view('kill'), name="api_vm_kill"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/start$" % self._meta.resource_name, self.wrap_view('start'), name="api_vm_start"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/stop$" % self._meta.resource_name, self.wrap_view('stop'), name="api_vm_stop"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
    def console(self, request, **kwargs):
         basic_bundle = self.build_bundle(request=request)
         vm = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
         return self.create_response(request, vm.console())
    def kill(self, request, **kwargs):
        if request.method == 'POST':
            basic_bundle = self.build_bundle(request=request)
            vm = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
            return self.create_response(request, vm.kill())
    def start(self, request, **kwargs):
        if request.method == 'POST':
            basic_bundle = self.build_bundle(request=request)
            vm = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
            return self.create_response(request, vm.start())
    def stop(self, request, **kwargs):
        if request.method == 'POST':
            basic_bundle = self.build_bundle(request=request)
            vm = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
            return self.create_response(request, vm.stop())

class StackResource(ModelResource):
    createdby        = fields.ForeignKey(CreatedByResource, 'createdby')
    class Meta:
        queryset       =  Stack.objects.all()
        authentication = StaffAuthentication()
        authorization  = DjangoAuthorization()
        detail_uri_name = 'name'
        collection_name = 'results'
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/kill$" % self._meta.resource_name, self.wrap_view('kill'), name="api_stack_kill"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/show$" % self._meta.resource_name, self.wrap_view('show'), name="api_stack_show"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/start$" % self._meta.resource_name, self.wrap_view('start'), name="api_stack_start"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/stop$" % self._meta.resource_name, self.wrap_view('stop'), name="api_stack_stop"),
            url(r"^(?P<resource_name>%s)/(?P<name>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
    def kill(self, request, **kwargs):
        if request.method == 'POST':
            basic_bundle = self.build_bundle(request=request)
            stack = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
            return self.create_response(request, stack.kill())
    def show(self, request, **kwargs):
         basic_bundle = self.build_bundle(request=request)
         stack = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
         return self.create_response(request, stack.show())
    def start(self, request, **kwargs):
        if request.method == 'POST':
            basic_bundle = self.build_bundle(request=request)
            stack = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
            return self.create_response(request, stack.start())
    def stop(self, request, **kwargs):
        if request.method == 'POST':
            basic_bundle = self.build_bundle(request=request)
            stack = self.cached_obj_get(bundle=basic_bundle,**self.remove_api_resource_names(kwargs))
            return self.create_response(request, stack.stop())
