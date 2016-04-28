from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from models import *    
from FratApp.models import *

# Create your views here.

def index(request):
    #load page if user is logged in, redirect to external landing page if not
    if request.user.is_authenticated():
        user = request.user
        #list of all ranks currently assigned to existing users
        allranks = set([x.rank for x in ExtraUserFields.objects.all()])
        noranks = set(["none", "NONE", "None"])
        if allranks - noranks == allranks:
            allranks.add("None")    
        context = {
            'username':user.username,
            'firstname':user.first_name,
            'lastname':user.last_name,
            'ranks':allranks,
        }
        context['brotherlist'] = [x.first_name + " " + x.last_name + "(" + x.username + ")" 
                                  for x in User.objects.all() 
                                  if x.first_name != "" and x.last_name != ""]
        if request.method == 'POST':
            print request.POST
        if request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/')
        if request.method == 'POST' and 'usernamesubmit' in request.POST:
            context['loginfailed'] = False
            context['accountdisabled'] = False
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
            if primaryminor == "" and secondaryminor != "":
                primaryminor = secondaryminor
                secondaryminor = ""
            if primaryminor == "":
                primaryminor = "None"
            graddate = request.POST['graddate']
            phonenumber = request.POST['phone']
            roll = request.POST['roll']
            rank = request.POST['rank']
            rankother = request.POST['other']
            bigbrother = ""
            if 'bigbrotherother' in request.POST:
                bigbrother = request.POST['bigbrotherother']
            if bigbrother == "":
                bigbrother = request.POST['bigbrother']
            if rankother != "":
                rank = rankother
            user_created = True
            allgroups = Group.objects.filter(name="All")
            allexists = allgroups.exists()
            allgroup = None
            if allexists:
                allgroup = allgroups[0]
            if not allexists: #create group containing all users
                allgroup = Group.objects.create(name="All")
                allgroup.save()
            if password != passwordconfirm:
                context['mismatchedpassword'] = True
                user_created = False
            if len(username) < 6:
                context['invalidusername'] = True
                user_created = False
            if User.objects.filter(username=username).exists():#check if user already exists
                context['usernameused'] = True
                user_created = False
            if len(password) < 8:
                context['invalidpassword'] = True
                user_created = False
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
        return render(request, 'LandingPage/index.html', context)
    else:
        return redirect('/?redirected=True')
