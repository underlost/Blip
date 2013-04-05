import logging
import datetime
import markdown

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, smart_str
from django.template.defaultfilters import slugify

class EntryManager(models.Manager):
	
	def published(self):
		return self.public().filter(pub_date__lte=datetime.datetime.now())
	
	def public(self):
		return super(EntryManager, self).get_query_set().filter(is_private=False)

def upload_original(instance, filename):
	return 'images/original/%s/%s' % (instance.id, filename)

def upload_thumb(instance, filename):
	return 'images/thumbnail/300/%s/%s' % (instance.id, filename)

class EntryType(models.Model):
	name 		= models.CharField(max_length=250)
	slug 		= models.SlugField(max_length=250)
	is_public 	= models.BooleanField(help_text=_("Should be checked if you want anyone to be able to post."), default=False)
	pub_date	= models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
	image 		= models.ImageField(blank=True, null=True, upload_to=upload_original)
	thumbnail 	= models.ImageField(blank=True, null=True, upload_to=upload_thumb)
	owner 		= models.ForeignKey(User, related_name='owned_entrytypes')
	members 	= models.ManyToManyField(User, blank=True, null=True, related_name='members_entrytypes')

	def __unicode__(self):
		return "%s" % (self.name)

	def get_absolute_url(self):
		return "/%s/%s/" % (self.owner, self.slug)
	
	def items(self):
		return Entry.objects.filter(entry_type=self)
	
	def create_thumbnail(self, content_type=None):
		# original code for this method came from
		# http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
		# If there is no image associated with this.
		# do not create thumbnail
		if not self.image:
			return

		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (300, 2500)

		DJANGO_TYPE = content_type if content_type else self.image.file.content_type

		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'

		# Open original photo which we want to thumbnail using PIL's Image
		image = Image.open(StringIO(self.image.read()))

		# We use our PIL Image object to create the thumbnail, which already
		# has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

		# Save the thumbnail
		temp_handle = StringIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)
		
		# Save image to a SimpleUploadedFile which can be saved into

		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
				temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)	
	
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(EntryType, self).save(*args, **kwargs)
		
	class Meta:
		ordering = ('-pub_date',)
		
		
class Entry(models.Model):
	body 		= models.TextField()
	body_html 	= models.TextField()
	pub_date 	= models.DateTimeField(verbose_name=_("Date posted"), auto_now_add=True)
	is_private 	= models.BooleanField(help_text=_("Should be checked if no one else should see this."), default=False)
	entry_type 	= models.ForeignKey(EntryType, blank=True, null=True)
	owner 		= models.ForeignKey(User, related_name='owned_entries')
	
	objects 	= EntryManager()
	
	def __unicode__(self):
		return self.body_html		
	
	def get_absolute_url(self):
		return "/%s/post/%s/" % (self.owner, self.id)
		
	class Meta:
		ordering = ('-pub_date',)
		verbose_name_plural = 'entries'
	
	def save(self, *args, **kwargs):
		self.body_html = markdown.markdown(smart_unicode(self.body))
		super(Entry, self).save(*args, **kwargs)