from __future__ import absolute_import

import hashlib
import json
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core import cache
from django.http import HttpResponse
from .forms import ProfileForm
from .models import Profile

from bloop.utils import profile

def user_profile(request, username):
    u = get_object_or_404(User, username=username)
    p = u.get_profile()
    ctx = {
        'user_obj': u,
        'profile_obj': p,
        'email_hash': hashlib.md5(u.email).hexdigest(),
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
    # Return info about some users as a JSON object.
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
