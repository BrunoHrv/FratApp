from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

import os
from os.path import abspath, dirname, join, normpath
from sys import path
from .models import *

SITE_ROOT_tmp = dirname(dirname(abspath(__file__)))
SITE_ROOT = SITE_ROOT_tmp[1:]

TEMPLATE_DIR = normpath('Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')

def index(request, redirected=False):
	if request.user.is_authenticated():#redirect user to internal landing page if they're already logged in
		return redirect('/LandingPage')
    	ind = normpath(join(TEMPLATE_DIR, 'index.html'))
	user = None
	allranks = set([x.rank for x in ExtraUserFields.objects.all()])
	noranks = set(["none","NONE","None"])
	if allranks - noranks == allranks:
		allranks.add("None")	
	context={
		'redirected':redirected,
		'ranks':allranks
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
	email = request.POST['email']
	firstname=request.POST['firstname']
	lastname=request.POST['lastname']
	hometown=request.POST['hometown']
	primarymajor=request.POST['primarymajor']
	secondarymajor=request.POST['secondarymajor']
	primaryminor=request.POST['primaryminor']
	secondaryminor=request.POST['secondaryminor']
	if primaryminor == "" and secondaryminor != "":
		primaryminor = secondaryminor
		secondaryminor=""
	if primaryminor =="":
		primaryminor="None"
	graddate=request.POST['graddate']
	phonenumber=request.POST['phone']
	roll=request.POST['roll']
	rank=request.POST['rank']
	rankother=request.POST['other']
	if rankother != "":
		rank=rankother
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
		userextras=ExtraUserFields.objects.create(brother=user,hometown=hometown,email=email,primarymajor=primarymajor, secondarymajor=secondarymajor,primaryminor=primaryminor, secondaryminor=secondaryminor,graduation_date=graddate,phonenumber=phonenumber,rollnumber=roll,rank=rank)
		user.first_name=firstname
		user.last_name=lastname
		user.groups=[allgroup]
		userextras.brother=user
		user.save()#save user to database
		userextras.save()
	context['usercreated']=user_created
	return render(request, 'index.html', context)
