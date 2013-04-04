from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'url', 'date_created')

admin.site.register(Profile, ProfileAdmin)