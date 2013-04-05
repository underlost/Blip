from __future__ import absolute_import

from django.conf.urls.defaults import patterns, url
from . import views as account_views

urlpatterns = patterns('',
  
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', account_views.logout_user, name='logout'),
    url(r'^register/$', account_views.register, name='register'),
   
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm', name='auth_password_reset_confim',),
    url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'),
  
    url(r'^edit/$', account_views.edit_profile, name='edit_profile',),
)