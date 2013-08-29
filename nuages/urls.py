from django.conf.urls import patterns, include, url
from django.contrib import admin
#specific stuff for auth
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
import django.contrib.auth



# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('portal.views',
    # Examples:
    # url(r'^$', 'nuages.views.home', name='home'),
    # url(r'^nuages/', include('nuages.foo.urls')),
      url(r'^nuages/$', 'create'),
      url(r'^nuages/vms/$', 'create'),
      url(r'^nuages/profiles/$', 'profiles'),
      url(r'^nuages/storage/$', 'storage'),
      url(r'^nuages/profileinfo/', 'profileinfo'),
      url(r'^nuages/virtualprovidertype/', 'virtualprovidertype'),
      url(r'^nuages/types/', 'types'),
      url(r'^nuages/hostgroups/', 'hostgroups'),
      url(r'^nuages/yourvms/$', 'yourvms'),
      url(r'^nuages/allvms/$', 'allvms'),
      url(r'^nuages/vms/console', 'console'),
      url(r'^nuages/vms/start', 'start'),
      url(r'^nuages/vms/stop', 'stop'),
      url(r'^nuages/vms/kill', 'kill'),
      url(r'^nuages/customforms', 'customforms'),
      url(r'^nuages/customformedit', 'customformedit'),
      url(r'^nuages/customforminfo', 'customforminfo'),
      url(r'^nuages/customformupdate','customformupdate'),
      url(r'^nuages/customformdelete','customformdelete'),
      #url(r'^nuages/addform', 'addform'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'} ),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login' ),
    )
