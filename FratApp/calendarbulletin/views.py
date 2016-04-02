from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Bulletin
import httplib2
import os
import apiclient
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build

#scopes = ['https://www.googleapis.com/auth/sqlservice.admin', 'https://www.googleapis.com/auth/calendar']
#credentials = ServiceAccountCredentials.from_json_keyfile_name('FratApp-3a6a3a856702.json', scopes=scopes)
#http_auth = credentials.authorize(Http())
#caladmin = build('calendar', 'v3', http=http_auth)
#APPLICATION_NAME = 'FratApp'

def index(request):
	if request.user.is_authenticated():
		user = request.user
		#delegated_credentials = credentials.create_delegated(user.email)
		#user_auth = delegated_credentials.authorize(Http())
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
		}
		print context
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		if request.method == 'POST' and 'addbulletin' in request.POST:
			Creator = user.first_name + ' ' + user.last_name
			Title = request.POST['title']
			Description = request.POST['description']
			announcement = Bulletin.objects.create(creator=Creator, title = Title, text = Description)
		context['bulletin_list'] = Bulletin.objects.all()

		return render(request, 'Calendar/index.html', context)
	else:
		return redirect('/?redirected=True')
