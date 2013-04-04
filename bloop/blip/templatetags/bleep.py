from __future__ import absolute_import
from urlparse import urlparse
import hashlib

from django import template
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User

from ..models import EntryType, Entry

register = template.Library()

@register.inclusion_tag('blip/templatetags/lists.html')
def render_lists(user, num):
	objects = EntryType.objects.filter(owner__username=user)[:num]
	return {'objects': objects,}

@register.filter
def base_site_url(value):                                        
	parsed = urlparse(value)
	return parsed.netloc

@register.filter
def email_hash(value):
	u = get_object_or_404(User, username=value)
	a = hashlib.md5(u.email).hexdigest()                                       
	return a
