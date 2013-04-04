from __future__ import absolute_import

import markdown
from django.utils.encoding import smart_unicode, smart_str
from django import forms
from django.forms import widgets
from .models import EntryType, Entry


class EntryTypeModelForm(forms.ModelForm):

    class Meta:
        model = EntryType
        exclude = ('pub_date', 'slug', 'owner', 'image', 'is_public', 'members')
        widgets = {		
        	'name': forms.TextInput(attrs={'class':'input-block-level', 'placeholder':'Title'}),
        }


class EntryModelForm(forms.ModelForm):
    
    class Meta:
        model = Entry
        exclude = ('pub_date', 'entry_type', 'owner', 'body_html')
        widgets = {		
        	'body': forms.Textarea(attrs={'class':'input-block-level'}),
        }