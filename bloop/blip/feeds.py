from __future__ import absolute_import

from django.core import urlresolvers
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from .models import EntryType, Entry