from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from signals import create_profile

from datetime import datetime

# When model instance is saved, trigger creation of corresponding profile
signals.post_save.connect(create_profile, sender=User)

GENDER_CHOICES = (
	('F', _('Female')),
	('M', _('Male')),
	('P', _('Pirate')),
	('N', _('Ninja')),
	('R', _('Robot')),
)

class Profile(models.Model):
    user 			  = models.OneToOneField(User)
    name              = models.CharField(max_length=200, blank=True)
    date_created      = models.DateTimeField(auto_now_add=True)
    gender			  = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    location 		  = models.CharField(max_length=255, blank=True, null=True)
    url				  = models.URLField(blank=True)
    about			  = models.TextField(blank=True)
    
    #Profile Settings
    hide_mobile       = models.BooleanField(default=False)
    last_seen_on      = models.DateTimeField(auto_now_add=True)
    preferences       = models.TextField(default="{}")
    view_settings     = models.TextField(default="{}")
    send_emails       = models.BooleanField(default=False)
    is_beta			  = models.BooleanField(default=True)
    
    #is_premium 	  = models.BooleanField(default=False)
    #secret_token 	  = models.CharField(max_length=12, blank=True, null=True)
    #stripe_4_digits  = models.CharField(max_length=4, blank=True, null=True)
    #stripe_id 		  = models.CharField(max_length=24, blank=True, null=True)

    def __unicode__(self):
        return self.name or unicode(self.user)
   
    @models.permalink 
    def get_absolute_url(self):
        return "/%s/" % (unicode(self.user.username))
