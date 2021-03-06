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

site_root_tmp = dirname(dirname(abspath(__file__)))
SITE_ROOT = site_root_tmp[1:]

TEMPLATE_DIR = normpath('Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')

def index(request, redirected=False):
    #redirect user to internal landing page if they're already logged in
    if request.user.is_authenticated():
        return redirect('/LandingPage')
        #ind = normpath(join(TEMPLATE_DIR, 'index.html'))
    user = None
    allranks = set([x.rank for x in ExtraUserFields.objects.all()])
    noranks = set(["none", "NONE", "None"])
    if allranks - noranks == allranks:
        allranks.add("None")    
    context = {
        'redirected' : redirected,
        'ranks' : allranks
    }
    #admins can control whether or not the general public can make their own accounts
    context['publicusercreation'] = False  
    context['publicbrotherlist'] = True and context['publicusercreation']
    if context['publicbrotherlist'] is True:
        context['brotherlist'] = [x.first_name + " " + x.last_name + "(" + x.username + ")" 
                                  for x in User.objects.all() 
                                  if x.first_name != "" and x.last_name != ""]
    if request.method == 'GET':
        if 'redirected' in request.GET:
            #see if user was redirected here for not being logged in
            context['redirected'] = request.GET['redirected']
            context['loginfailed'] = False
            context['accountdisabled'] = False
        return render(request, 'index.html', context)
    if request.method == 'POST' and 'login' in request.POST: #user is trying to log in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:#log them in
                login(request, user)
                return redirect('/LandingPage')
            else:#account disabled
                context['loginfailed'] = False
                context['accountdisabled'] = True
                return render(request, 'index.html', context)
        else:#bad credentials
            context['loginfailed'] = True
            context['accountdisabled'] = False
            return render(request, 'index.html', context)
    context['loginfailed'] = False
    context['accountdisabled'] = False
    #If the code reaches this far, the user is trying to create a new user
    username = request.POST['usernamesubmit']
    password = request.POST['passwordsubmit']
    passwordconfirm = request.POST['passwordconfirmation']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    hometown = request.POST['hometown']
    primarymajor = request.POST['primarymajor']
    secondarymajor = request.POST['secondarymajor']
    primaryminor = request.POST['primaryminor']
    secondaryminor = request.POST['secondaryminor']
    #If the user inputted a secondaryminor but not a primary, have primary register as secondary
    if primaryminor == "" and secondaryminor != "":
        primaryminor = secondaryminor
        secondaryminor = ""
    if primaryminor == "":
        primaryminor = "None"
    user_created = True
    graddate = request.POST['graddate']
    try:
        graddate = datetime.datetime.strptime(graddate,'%Y-%m-%d')
    except ValueError:
        user_created = False
        context['badDate'] = True
    phonenumber = request.POST['phone']
    roll = request.POST['roll']
    rank = request.POST['rank']
    rankother = request.POST['other']
    bigbrother = ""
    #Set the user's big brother
    if 'bigbrotherother' in request.POST:
        bigbrother = request.POST['bigbrotherother']
    if bigbrother == "":
        bigbrother = request.POST['bigbrother']
    if rankother != "":
        rank = rankother
    allgroups = Group.objects.filter(name="All")
    allexists = allgroups.exists()
    allgroup = None
    if allexists:
        allgroup = allgroups[0]
    #create group containing all users if it doesn't already exist
    if not allexists: 
        allgroup = Group.objects.create(name="All")
        allgroup.save()
    #Check that the inputted passwords match
    if password != passwordconfirm:
        context['mismatchedpassword'] = True
        user_created = False
    #Check username validity
    if len(username) < 6:
        context['invalidusername'] = True
        user_created = False
    #check if user already exists
    if User.objects.filter(username=username).exists():
        context['usernameused'] = True
        user_created = False
    #Check the password validity
    if len(password) < 8:
        context['invalidpassword'] = True
        user_created = False
    #Actually create and register the user in our database
    if user_created:
        user = User.objects.create_user(username, email, password)
        userextras = ExtraUserFields.objects.create(
            brother=user,
            hometown=hometown,
            primarymajor=primarymajor, 
            secondarymajor=secondarymajor,
            primaryminor=primaryminor, 
            secondaryminor=secondaryminor,
            graduation_date=graddate,
            phonenumber=phonenumber,
            rollnumber=roll,
            rank=rank,
            bigbrother=bigbrother)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.groups = [allgroup]
        userextras.brother = user
        user.save()#save user to database
        userextras.save()
    context['usercreated'] = user_created
    return render(request, 'index.html', context)
