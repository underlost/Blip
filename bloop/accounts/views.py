import hashlib
import json

from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import cache

from .forms import ProfileForm, UserCreationForm
from .models import Profile

def register(request):
    if not settings.ALLOW_NEW_REGISTRATIONS:
        messages.error(request, "The admin of this service is not "
                                "allowing new registrations.")
        return HttpResponseRedirect(reverse('aggregator:index'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Thanks for registering. You are now logged in.')
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = UserCreationForm()

    return TemplateResponse(request, 'registration/registration_form.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('index'))


def user_profile(request, username):
    u = get_object_or_404(User, username=username)
    ctx = {
        'user_obj': u,
        'email_hash': hashlib.md5(u.email).hexdigest(),
        'user_can_commit': u.has_perm('auth.commit'),
    }
    return render(request, "accounts/user_profile.html", ctx)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('user_profile', request.user.username)
    return render(request, "accounts/edit_profile.html", {'form': form})

def json_user_info(request):
    """
    Return info about some users as a JSON object.

    Part of a set of hacks that feed more info into Trac. This takes
    a list of users as GET['user'] and returns a JSON object::

        {
            {USERNAME: {"core": false, "cla": true}},
            {USERNAME: {"core": false, "cla": true}},
            ...
        }

    De-duplication on GET['user'] is performed since I don't want to have to
    think about how best to do it in JavaScript :)
    """

    userinfo = dict([
                (name, get_user_info(name))
                for name in set(request.GET.getlist('user'))])
    return JSONResponse(userinfo)

def get_user_info(username):
    c = cache.get_cache('default')
    username = username.encode('ascii', 'ignore')
    key = 'trac_user_info:%s' % hashlib.md5(username).hexdigest()
    info = c.get(key)
    if info is None:
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            info = {"core": False, "cla": False}
        else:
            info = {
                "core": u.has_perm('auth.commit'),
                "cla": bool(find_agreements(u))
            }
        c.set(key, info, 60*60)
    return info

class JSONResponse(HttpResponse):
    def __init__(self, obj):
        super(JSONResponse, self).__init__(
            json.dumps(obj, indent=(2 if settings.DEBUG else None)),
            content_type='application/json',
        )
