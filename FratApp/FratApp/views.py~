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

def index(request, redirected=False):
    	ind = normpath(join(TEMPLATE_DIR, 'index.html'))
	user = None
	context={
		'redirected':redirected,
	}
	if request.method == 'GET':
		if 'redirected' in request.GET:
			context['redirected']=request.GET['redirected']
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
	context['loginfailed']=False
	context['accountdisabled']=False
	username=request.POST['usernamesubmit']
	password=request.POST['passwordsubmit']
	passwordconfirm=request.POST['passwordconfirmation']
	firstname=request.POST['firstname']
	lastname=request.POST['lastname']
	if password != passwordconfirm:
		context['mismatchedpassword']=True
	if len(username) < 6:
		context['invalidusername']=True
	if len(username) < 6:#change
		context['usernameused']=True
	if len(password) < 8:
		context['invalidpassword']=True
