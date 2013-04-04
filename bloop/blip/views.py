from __future__ import absolute_import

import logging
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list

from .models import EntryType, Entry
from .forms import EntryTypeModelForm, EntryModelForm

def index(request):
	#Displays global feed
	ctx = {'entry_list': Entry.objects.all()[:50]}
	return render(request, 'blip/index.html', ctx)

def lists(request):
	#Displays the latest entries of each type.
	ctx = {'entrytype_list': EntryType.objects.all()}
	return render(request, 'blip/lists.html', ctx)

def lists_for_user(request, username):
	#Shows the latest entries for a given user.
	ctx = {'entrytype_list': EntryType.objects.filter(owner__username=username)}
	return render(request, 'blip/lists_for_user.html', ctx)

def entry_list(request, username, entry_type_slug):
	#Shows the latest entries for a given list.
	entry_type = get_object_or_404(EntryType, slug=entry_type_slug, owner__username=username)
	return object_list(request,
		queryset = Entry.objects.filter(entry_type=entry_type, is_private=False),
		paginate_by = 25,
		extra_context = {'entry_type': entry_type},
	)

def entry(request, username, entry_id):
	#Shows a single entry.
	entry = get_object_or_404(Entry, id=entry_id, owner__username=username)
	ctx = {'entry': entry}
	return render(request, 'blip/entry.html', ctx)

@login_required
def mine(request):
	#Lets the user see, edit, and delete all of their owned entries.
	entry_types = EntryType.objects.filter(owner=request.user)
	if not request.user.is_superuser:
		entry_types = entry_types.filter(is_public=True)

	ctx = {
		'entries': Entry.objects.filter(owner=request.user),
		'entry_types': entry_types
	}
	return render(request, 'blip/my-entries.html', ctx)


@login_required
def my_entries(request):
	#Lets the user see, edit, and delete all of their owned entries.
	entry_types = EntryType.objects.all()
	if not request.user.is_superuser:
		entry_types = entry_types.filter(is_public=True)

	ctx = {
		'entries': Entry.objects.filter(owner=request.user),
		'entry_types': entry_types
	}
	return render(request, 'blip/my-entries.html', ctx)

@login_required
def add_entry_to_list(request, username, entry_type_slug):
	#Lets user add new enties to a list.
	ft = get_object_or_404(EntryType, slug=entry_type_slug, owner__username=username)
	if not ft.is_public and not request.user.is_superuser:
		return render(request, 'blip/denied.html')

	instance = Entry(entry_type=ft, owner=request.user)
	f = EntryModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Entry Posted.')
		return redirect('blip-entry-list', username=username, entry_type_slug=entry_type_slug)

	ctx = {'form': f, 'entry_type': ft, 'adding': True}
	return render(request, 'blip/edit-entry.html', ctx)

@login_required
def add_list(request):
	#add an entry.
	instance = EntryType(owner=request.user)
	f = EntryTypeModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'New list created.')
		return redirect('blip-index')

	ctx = {'form': f, 'adding': True}
	return render(request, 'blip/add-list.html', ctx)	

@login_required
def add_entry(request):
	#add an entry.
	instance = Entry(owner=request.user)
	f = EntryModelForm(request.POST or None, instance=instance)
	if f.is_valid():
		f.save()
		messages.add_message(
			request, messages.INFO, 'Entry Posted.')
		return redirect('blip-index')

	ctx = {'form': f, 'adding2': True}
	return render(request, 'blip/edit-entry.html', ctx)	

@login_required
def edit_entry(request, entry_id):
	#Lets a user edit an entry they've previously added.
	#Only entries the user "owns" can be edited.
	entry = get_object_or_404(Entry, pk=entry_id, owner=request.user)
	f = EntryModelForm(request.POST or None, instance=entry)
	if f.is_valid():
		f.save()
		return redirect('blip-my-entries')

	ctx = {'form': f, 'entry': entry, 'adding': False}
	return render(request, 'blip/edit-entry.html', ctx)

@login_required
def delete_entry(request, entry_id):
	#Lets a user delete an entry they've previously added.
	#Only entries the user "owns" can be deleted.
	entry = get_object_or_404(Entry, pk=entry_id, owner=request.user)
	if request.method == 'POST':
		entry.delete()
		return redirect('blip-my-entries')
	return render(request, 'blip/delete-confirm.html', {'entry': entry})
