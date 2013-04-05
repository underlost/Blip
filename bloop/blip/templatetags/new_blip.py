from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext

from bloop.blip.forms import EntryModelForm

register = Library()


@register.inclusion_tag('blip/templatetags/new_blip.html')
def new_blip(request):
	return {'form': EntryModelForm(),}

@register.simple_tag
def new_blip(request):
    return render_to_string('blip/templatetags/new_blip.html', {'form': EntryModelForm()}, context_instance=RequestContext(request))
