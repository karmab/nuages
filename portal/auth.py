# import the User object
from django.contrib.auth.models import User
from portal.models import LdapProvider
import ldap
import logging
import sys
import os
import socket

class LdapBackend(object):
	def authenticate(self, username=None, password=None):
		success = False
		#logging.debug("prout")
		ldap.set_option(ldap.OPT_NETWORK_TIMEOUT , 10 )
		ldap.set_option ( ldap.OPT_REFERRALS , 0 )
		ldapproviders=LdapProvider.objects.all()
		for provider in ldapproviders:
			port = 389
			host,basedn,binddn,bindpassword,secure,userfield,filter,certname=provider.host,provider.basedn,provider.binddn,provider.bindpassword,provider.secure,provider.userfield,provider.filter,provider.certname
			ldapuri="ldap://%s" % (host)
			if secure:
				port = 636
				pwd = os.environ["PWD"]
				cert="%s/%s" % (pwd,certname)
				ldapuri="ldaps://%s" % (host)
				ldap.set_option( ldap.OPT_X_TLS_CACERTFILE , cert )
				ldap.set_option( ldap.OPT_X_TLS_REQUIRE_CERT , ldap.OPT_X_TLS_ALLOW)
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.settimeout(5)
				sock.connect((host, port))
			except socket.error:
				print "unreachable host %s, continuing" % host
				continue
			userfilter = "%s=%s" % (userfield,username)
			if filter:
				userfilter="(&(%s)(%s))" % (userfilter,filter)
			attrs = [str(userfield)]
			try:
				c = ldap.initialize(ldapuri)
				c.simple_bind_s(binddn,bindpassword)
				res=c.search_s( basedn, ldap.SCOPE_SUBTREE, userfilter, attrs)
				c.unbind()
			except:	
				continue
			if res[0]:
				usercn=res[0][0]
				try:
					c = ldap.initialize(ldapuri)
					c.simple_bind_s(usercn,password)
					c.unbind()
					success = True
					break
				except:	
					continue
		if not success:
			#if we have looped through all ldap providers and not been able to authenticate,exit
			return None		
		else:
			user, created = User.objects.get_or_create(username=username)
			if created:
				print "created %s" % username
			return user

	def get_user(self, user_id):
        	try:
            		return User.objects.get(pk=user_id)
        	except User.DoesNotExist:
            		return None
