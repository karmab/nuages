# import the User object
from django.contrib.auth.models import User
from portal.models import LdapProvider
import ldap
import logging
import sys
import os
import socket
from django.conf import settings


class LdapBackend(object):
	def authenticate(self, username=None, password=None):
		success = False
		ldap.set_option(ldap.OPT_NETWORK_TIMEOUT , 10 )
		ldap.set_option ( ldap.OPT_REFERRALS , 0 )
		ldapproviders=LdapProvider.objects.all()
		for provider in ldapproviders:
			port = 389
			host, basedn, binddn, bindpassword, secure, userfield,certname, filter1, filter2, filter3, filter4, groups1, groups2, groups3, groups4 = provider.host, provider.basedn, provider.binddn, provider.bindpassword, provider.secure, provider.userfield, provider.certname, provider.filter1, provider.filter2, provider.filter3, provider.filter4, provider.groups1, provider.groups2, provider.groups3, provider.groups4
			activefilters=[]
			for filter in [filter1,filter2,filter3,filter4]:
				if filter:
					activefilters.append(filter)
			ldapuri="ldap://%s" % (host)
			if secure:
				port = 636
				pwd = settings.PWD
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
			try:
				c = ldap.initialize(ldapuri)
				c.simple_bind_s(binddn,bindpassword)
				if not activefilters:
					res=c.search_s( basedn, ldap.SCOPE_SUBTREE, userfilter, attrs)
				else:
					for filter in activefilters:
						userfilter="(&(%s)(%s))" % (userfilter,filter)
						attrs = [str(userfield)]
						res=c.search_s( basedn, ldap.SCOPE_SUBTREE, userfilter, attrs)
						if res[0]:
							activefilters = filter
							break
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
				if groups1.values() and not filter1:
					for group in groups1.values():
						user.groups.add(group['id'])
					user.save()
				if filter and filter==filter1 and groups1.values():
					for group in groups1.values():
						user.groups.add(group['id'])
					user.save()
				if filter and filter==filter2 and groups2.values():
					for group in groups2.values():
						user.groups.add(group['id'])
					user.save()
				if filter and filter==filter3 and groups3.values():
					for group in groups3.values():
						user.groups.add(group['id'])
					user.save()
				if filter and filter==filter4 and groups4.values():
					for group in groups4.values():
						user.groups.add(group['id'])
					user.save()
			return user

	def get_user(self, user_id):
        	try:
            		return User.objects.get(pk=user_id)
        	except User.DoesNotExist:
            		return None
