from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import User
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    A form for editing user profiles.

    Assumes that the Profile instance passed in has an associated User
    object. The view (see views.py) takes care of tha
    """
    class Meta(object):
        model = Profile
        fields = ['name']
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {}).update({'email': instance.user.email})
        super(ProfileForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ProfileForm, self).save(commit=commit)
        if 'email' in self.cleaned_data:
            instance.user.email = self.cleaned_data['email']
            if commit:
                instance.user.save()
        return instance


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w-]+$')
    password = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user