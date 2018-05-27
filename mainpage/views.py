# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry
from .forms import TopicForm,EntryForm
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
	if request.user.is_authenticated():		
		topics = Topic.objects.filter(owner = request.user).order_by('date_added')
		context = {'topics':topics}
		return render(request,'mainpage/index.html',context)
	else:
		return render(request,'mainpage/index.html')

# This is not used now
@login_required
def topics(request):
	topics = Topic.objects.filter(owner = request.user).order_by('date_added')
	context = {'topics':topics}
	#return render(request,'mainpage/topics.html',context)
	return render(request,'mainpage/base.html',context)

@login_required
def topic(request,topic_id):
	topics = Topic.objects.filter(owner = request.user).order_by('date_added')
	topic = get_object_or_404(Topic,id = topic_id)
#	topic = Topic.objects.get(id = topic_id)
	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries, 'topics':topics}
	return render(request,'mainpage/topic.html',context)

@login_required
def new_topic(request):
	topics = Topic.objects.filter(owner = request.user).order_by('date_added')
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit = False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('mainpage:topics'))
	context = {'form':form,'topics':topics}
	return render(request,'mainpage/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
	topics = Topic.objects.filter(owner = request.user).order_by('date_added')
	topic = Topic.objects.get(id = topic_id)
	if topic.owner != request.user:
		raise Http404

	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data = request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('mainpage:topic',args=[topic_id]))
	context = {'topic':topic,'form':form,'topics':topics}
	return render(request,'mainpage/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
	topics = Topic.objects.filter(owner = request.user).order_by('date_added')
	entry = Entry.objects.get(id = entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404
	
	if request.method != 'POST':
		form = EntryForm(instance = entry)
		
	else: 
		form = EntryForm(instance = entry, data = request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('mainpage:topic',args=[topic.id]))
	context = {'entry':entry,'topic':topic, 'form':form,'topics':topics}
	return render(request,'mainpage/edit_entry.html',context)
