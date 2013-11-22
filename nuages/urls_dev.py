from django.conf.urls import patterns, include, url
from django.contrib import admin
#specific stuff for auth
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('portal.views',
    # Examples:
    # url(r'^$', 'nuages.views.home', name='home'),
    # url(r'^nuages/', include('nuages.foo.urls')),
      url(r'^nuages/$', 'create'),
      url(r'^nuages/vms/$', 'create', name='create'),
      url(r'^nuages/vms/findvm', 'findvm', name='findvm'),
      url(r'^nuages/profiles/$', 'profiles', name='profiles'),
      url(r'^nuages/profilecopy/$', 'profilecopy',name='profilecopy'),
      url(r'^nuages/storage/$', 'storage',name='storage'),
      url(r'^nuages/profileinfo/', 'profileinfo',name='profileinfo'),
      url(r'^nuages/virtualprovidertype/', 'virtualprovidertype', name='virtualprovidertype'),
      url(r'^nuages/types/', 'types', name='types'),
      url(r'^nuages/hostgroups/', 'hostgroups', name='hostgroups'),
      url(r'^nuages/yourvms/$', 'yourvms', name='yourvms'),
      url(r'^nuages/allvms/$', 'allvms', name='allvms'),
      url(r'^nuages/vms/console', 'console', name='console'),
      url(r'^nuages/vms/start', 'start', name='start'),
      url(r'^nuages/vms/stop', 'stop', name='stop'),
      url(r'^nuages/vms/kill', 'kill', name='kill'),
      url(r'^nuages/vms/dbremove', 'dbremove', name='dbremove'),
      url(r'^nuages/customforms', 'customforms', name='customforms'),
      url(r'^nuages/customformedit', 'customformedit', name='customformedit'),
      url(r'^nuages/customforminfo', 'customforminfo', name='customforminfo'),
      url(r'^nuages/customformupdate','customformupdate', name='customformupdate'),
      url(r'^nuages/customformcreate','customformcreate', name='customformcreate'),
      url(r'^nuages/customformdelete','customformdelete', name='customformdelete'),
      url(r'^nuages/invoicepdf','invoicepdf', name='invoicepdf'),
      url(r'^nuages/invoice','invoice', name='invoice'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^nuages/admin/', include(admin.site.urls)),
    url(r'^nuages/login/$', 'portal.views.customlogin', {'template_name': 'login.html'} , name='login'),
    url(r'^nuages/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout' ),
    )
