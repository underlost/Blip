from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings

from bloop.accounts import views as account_views

admin.autodiscover()
handler500 = 'bloop.views.server_error'

urlpatterns = patterns('',

	#Static
	
	url(r'^about/$', TemplateView.as_view(template_name="static/about.html") name="about"),
	url(r'^api/$', TemplateView.as_view(template_name="static/api.html") name="api"),
	
	#Apps
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('bloop.blip.urls')),
	
	#User
	url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}, name='login'),
	url(r'^logout/$', account_views.logout_user, name='logout'),
	url(r'^register/$', account_views.register, name='registration_register'),
	url(r'^reset/$', 'django.contrib.auth.views.password_reset', {'template_name': 'registration/reset.html'}, name='auth_password_reset'),
	url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm', name='auth_password_reset_confim',),
	url(r'^reset/done/$','django.contrib.auth.views.password_reset_complete'),
	
	url(r'^settings/$', account_views.edit_profile, name='edit_profile',),
	url(r'^(?P<username>[\w-]+)/$', account_views.user_profile, name='user_profile'),	
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)