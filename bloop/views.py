from __future__ import absolute_import

from django.contrib.comments.models import Comment
from django.contrib.sitemaps import views as sitemap_views
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template


@requires_csrf_token
def server_error(request, template_name='500.html'):
    #Custom 500 error handler for static stuff.
    return render(request, template_name)