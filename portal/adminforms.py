#-*- coding: utf-8 -*-
import os
from django.forms import ModelForm, PasswordInput
from portal.models import *

class VirtualProviderForm(ModelForm):
    class Meta:
        model = VirtualProvider
        widgets = {
            'password': PasswordInput(),
        }

class PhysicalProviderForm(ModelForm):
    class Meta:
        model = PhysicalProvider
        widgets = {
            'password': PasswordInput(),
        }

class LdapProviderForm(ModelForm):
    class Meta:
        model = LdapProvider
        widgets = {
            'bindpassword': PasswordInput(),
        }

class IpamProviderForm(ModelForm):
    class Meta:
        model = IpamProvider
        widgets = {
            'password': PasswordInput(),
        }

class ForemanProviderForm(ModelForm):
    class Meta:
        model = ForemanProvider
        widgets = {
            'password': PasswordInput(),
        }

class CobblerProviderForm(ModelForm):
    class Meta:
        model = CobblerProvider
        widgets = {
            'password': PasswordInput(),
        }
