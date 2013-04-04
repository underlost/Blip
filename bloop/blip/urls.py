from __future__ import absolute_import

from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',

	#Global feed of all blips. 
    url(r'^$', views.index, name = 'blip-index'),
    
    #All public lists
    url(r'^lists/$', views.lists, name = 'blip-lists'),
    
    #Create a new list
    url(r'^lists/add/$', views.add_list, name = 'blip-add-list'),
    
    #Entries belonging to logged in user.
    url(r'^mine/$', views.my_entries, name = 'blip-my-entries' ),
    
    #A single blip.
    url(r'^(?P<username>[\w-]+)/post/(?P<entry_id>\d+)/$', views.entry, name = 'blip'),
    
    #List of blips
    url(r'^(?P<username>[\w-]+)/lists/$', views.lists_for_user, name = 'blip-user-lists'),
    url(r'^(?P<username>[\w-]+)/(?P<entry_type_slug>[-\w]+)/$', views.entry_list, name = "blip-entry-list"),
    
    #Post a blip.
    url(r'^post/$', views.add_entry, name = 'blip-add-entry'),
    
    #Edit Blip
    url(r'^post/(?P<entry_id>\d+)/edit/$', views.edit_entry, name = 'blip-edit-entry'),
    
    #Delete Blip
    url(r'^post/(?P<entry_id>\d+)/delete/$', views.delete_entry,name = 'blip-delete-entry'),
        
    #Add blip to sepcific list.
    url(r'^post/(?P<username>[\w-]+)/(?P<entry_type_slug>[-\w]+)/$', views.add_entry_to_list, name = 'blip-add-entry-to-list'),
    
)

