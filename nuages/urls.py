from django.conf.urls import patterns, include, url
from django.contrib import admin
#specific stuff for auth
from django.conf.urls.defaults import *
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

urlpatterns = patterns('portal.views',
      #url(r'^$', 'create'),
      url(r'^$', RedirectView.as_view(url=reverse_lazy('create'))),
      url(r'^vms/$', 'create', name='create'),
      url(r'^vms/findvm', 'findvm', name='findvm'),
      url(r'^vms/quickvms/$', 'quickvms', name='quickvms'),
      url(r'^profiles/$', 'profiles', name='profiles'),
      url(r'^profilecopy/$', 'profilecopy', name='profilecopy'),
      url(r'^storage/$', 'storage', name='storage'),
      url(r'^profileinfo/', 'profileinfo', name='profileinfo'),
      url(r'^templateprofile/$', 'templateprofile', name='templateprofile'),
      url(r'^templateslist/$', 'templateslist', name='templateslist'),
      url(r'^createtemplateprofile/$', 'createtemplateprofile', name='createtemplateprofile'),
      url(r'^virtualprovidertype/', 'virtualprovidertype', name='virtualprovidertype'),
      url(r'^types/', 'types', name='types'),
      url(r'^hostgroups/', 'hostgroups', name='hostgroups'),
      url(r'^yourvms/$', 'yourvms', name='yourvms'),
      url(r'^allvms/$', 'allvms', name='allvms'),
      url(r'^vms/console', 'console', name='console'),
      url(r'^vms/start', 'start', name='start'),
      url(r'^vms/stop', 'stop', name='stop'),
      url(r'^vms/kill', 'kill', name='kill'),
      url(r'^vms/dbremove', 'dbremove', name='dbremove'),
      url(r'^customforms', 'customforms', name='customforms'),
      url(r'^customformedit', 'customformedit', name='customformedit'),
      url(r'^customforminfo', 'customforminfo', name='customforminfo'),
      url(r'^customformupdate','customformupdate', name='customformupdate'),
      url(r'^customformcreate','customformcreate', name='customformcreate'),
      url(r'^customformdelete','customformdelete', name='customformdelete'),
      url(r'^invoicepdf','invoicepdf', name='invoicepdf'),
      url(r'^invoice','invoice', name='invoice'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^login/$', 'portal.views.customlogin', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    )
