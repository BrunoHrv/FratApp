from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import datetime 
from django.utils import timezone

def index(request):
	if request.user.is_authenticated():
		user = request.user
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
		}
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		#Creation of a bulletin via a POST request
		if request.method == 'POST' and 'addbulletin' in request.POST:
			Creator = user.username
			Title = request.POST['title']
			Description = request.POST['description']
			expiration= request.POST['expiration']
			announcement = Bulletin.objects.create(creator=Creator, title = Title, text = Description, expiration_date = expiration)
		checks = BulletinClearer.objects.all()
		bc = None
		#Code to make certain that there is only one BulletinClearer in the database at once
		if len(checks) == 0:
			bc = BulletinClearer.objects.create()
		else:
			bc = checks[len(checks)-1]
			for c in checks:
				if c != bc:
					c.delete()
		#BulletinClearer checks to see if any bulletins need to be cleared
		bc.Clear_Bulletins()
		bulletin_list = Bulletin.objects.all()
		paginator = Paginator(bulletin_list, 10)
		page = request.GET.get('page')
		try:
			bulletins = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			bulletins = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			bulletins = paginator.page(paginator.num_pages)
		context['bulletins'] = bulletins
		return render(request, 'Calendar/index.html', context)
	else:
		return redirect('/?redirected=True')
