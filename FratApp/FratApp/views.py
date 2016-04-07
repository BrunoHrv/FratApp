from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

import os
from os.path import abspath, dirname, join, normpath
from sys import path

SITE_ROOT_tmp = dirname(dirname(abspath(__file__)))
SITE_ROOT = SITE_ROOT_tmp[1:]

TEMPLATE_DIR = normpath('Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')

def index(request, redirected=False):
	if request.user.is_authenticated():#redirect user to internal landing page if they're already logged in
		return redirect('/LandingPage')
    	ind = normpath(join(TEMPLATE_DIR, 'index.html'))
	user = None
	context={
		'redirected':redirected,
	}
	if request.method == 'GET':
		if 'redirected' in request.GET:
			context['redirected']=request.GET['redirected']#see if user was redirected here for not being logged in
		context['loginfailed']=False
		context['accountdisabled']=False
    		return render(request, 'index.html', context)
	if  'username' in request.POST and 'password' in request.POST:#user trying to log in
    		username = request.POST['username']
    		password = request.POST['password']
    		user = authenticate(username=username, password=password)
    		if user is not None:
    			if user.is_active:#log them in
            			login(request, user)
				return redirect('/LandingPage')
        		else:#account disabled
				context['loginfailed']=False
				context['accountdisabled']=True
    				return render(request, 'index.html', context)
    		else:#bad credentials
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
	user_created=True
	allgroups= Group.objects.filter(name="All")
	allexists=allgroups.exists()
	allgroup=None
	if allexists:
		allgroup=allgroups[0]
	if not allexists:#create group containing all users
		allgroup=Group.objects.create(name="All")
		allgroup.save()
	if password != passwordconfirm:
		context['mismatchedpassword']=True
		user_created=False
	if len(username) < 6:
		context['invalidusername']=True
		user_created=False
	if User.objects.filter(username=username).exists():#check if user already exists
		context['usernameused']=True
		user_created=False
	if len(password) < 8:
		context['invalidpassword']=True
		user_created=False
	if user_created:
		user = User.objects.create_user(username, None, password)
		user.first_name=firstname
		user.last_name=lastname
		user.groups=[allgroup]
		user.save()#save user to database
	context['usercreated']=user_created
	return render(request, 'index.html', context)
