from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings

from bloop.accounts import views as account_views

admin.autodiscover()
handler500 = 'bloop.views.server_error'

urlpatterns = patterns('',

	#Static
	url(r'^about/$', direct_to_template, {"template": "static/about.html"}, name="about"),
	url(r'^api/$', direct_to_template, {"template": "static/api.html"}, name="api"),
	
	#Apps
	url(r'^admin/', include(admin.site.urls)),
	url(r'^account/', include('bloop.accounts.urls')),
	url(r'^accounts/', include('registration.urls')),
	url(r'^', include('bloop.blip.urls')),
	
	#Profiles
	url(r'^(?P<username>[\w-]+)/$', account_views.user_profile, name='user_profile'),	
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)