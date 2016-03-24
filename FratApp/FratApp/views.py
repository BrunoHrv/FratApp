from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

import os
from os.path import abspath, dirname, join, normpath
from sys import path

SITE_ROOT_tmp = dirname(dirname(abspath(__file__)))
SITE_ROOT = SITE_ROOT_tmp[1:]

TEMPLATE_DIR = normpath('Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')
#TEMPLATE_DIR = normpath('C:/Users/jacobn2/Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')#normpath(join(SITE_ROOT, 'FratApp/templates'))

def index2(request, redirected=False):
	if request.user.is_authenticated():
		return redirect('/LandingPage')
    	ind = normpath(join(TEMPLATE_DIR, 'index.html'))
    	return render(request, 'index.html', {})
    	#return render(request, 'index.html', {})
#HttpResponse("Hello, world. You're at the main index.")


def index(request, redirected=False):
    	ind = normpath(join(TEMPLATE_DIR, 'index.html'))
	user = None
	context={
		'redirected':redirected,
	}
	if request.method == 'GET':
		context['loginfailed']=False
		context['accountdisabled']=False
    		return render(request, 'index.html', context)
	if  'username' in request.POST and 'password' in request.POST:
    		username = request.POST['username']
    		password = request.POST['password']
    		user = authenticate(username=username, password=password)
    	if user is not None:
    		if user.is_active:
            		login(request, user)
			return redirect('/LandingPage')
        	else:
			context['loginfailed']=False
			context['accountdisabled']=True
    			return render(request, 'index.html', context)
    	else:
		context['loginfailed']=True
		context['accountdisabled']=False
    		return render(request, 'index.html', context)
