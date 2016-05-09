from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from FratApp.models import *
import datetime
from django.contrib.auth import hashers 

# Create your views here.

def index(request):
    #Checks to see if logged. Sends back to index page if not logged in
    if request.user.is_authenticated():
        user = request.user
        isAdmin = True
        if hasattr(user,'extrauserfields'):
            isAdmin = user.extrauserfields.getAdminPermissions('user')
        context = {
            'username':user.username,
            'firstname':user.first_name,
            'lastname':user.last_name,
            'isAdmin':isAdmin,
        }
        #Recieve information from hypertext protocol
        if request.method == 'GET':
            #get specific user
            if 'user' in request.GET:
                userquery = User.objects.filter(username=request.GET['user'])
                if userquery.exists():
                    userquery=userquery[0]
                    context['userquery'] = userquery
                    context['majors'] = userquery.extrauserfields.getMajorsString()
                    context['minors'] = userquery.extrauserfields.getMinorsString()
                    if request.GET['user'] == user.username:
                        context['viewingSelf']=True
                        context['isAdmin']=True
                    return render(request, 'Directory/user.html', context)
                else:
                    context['userdoesnotexist']="There is no user named "+request.GET['user']
        #Logs out if requested, directs to main page if 'POST'
        if request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/')
        #Modification of a user via a POST request
        if request.method == 'POST' and 'modify_user' in request.POST:
            username = request.POST['username']
            userquery=User.objects.filter(username=username)[0]
            password = request.POST['passwordsubmit']
            passwordconfirm = request.POST['passwordconfirmation']
            email = request.POST['email']
            hometown = request.POST['hometown']
            primarymajor = request.POST['primarymajor']
            secondarymajor = request.POST['secondarymajor']
            primaryminor = request.POST['primaryminor']
            secondaryminor = request.POST['secondaryminor']
            graduation_date = request.POST['graddate']
            if graduation_date != "":
                try:
                    graddate = datetime.datetime.strptime(graduation_date,'%Y-%m-%d')
                    userquery.extrauserfields.graduation_date = graddate
                    userquery.extrauserfields.save()
                    userquery.save()
                except ValueError:
                    context['badDate'] = True
            phonenumber = request.POST['phone']
            rollnumber = request.POST['roll']
            rank=""
            if 'rank' in request.POST:
                rank = request.POST['rank']
            else:
                rank = request.POST['other']
            if password != passwordconfirm:
                context['mismatchedpassword'] = True
            #Check for password validity
            if len(password) > 0 and len(password) < 8:
                context['invalidpassword'] = True
            elif password == passwordconfirm:
                userquery.password = hashers.make_password(password)
                userquery.save()
            if email != "":
                userquery.email = email
                userquery.save()
            if hometown != "":
                userquery.extrauserfields.hometown = hometown
                userquery.extrauserfields.save()
                userquery.save()
            if primarymajor != "":
                userquery.extrauserfields.primarymajor = primarymajor
                userquery.extrauserfields.save()
                userquery.save()
            if secondarymajor != "":
                userquery.extrauserfields.secondarymajor = secondarymajor
                userquery.extrauserfields.save()
                userquery.save()
            if primaryminor != "":
                userquery.extrauserfields.primaryminor = primaryminor
                userquery.save()
                userquery.extrauserfields.save()
            if secondaryminor != "":
                if userquery.extrauserfields.primaryminor == "":
                    userquery.extrauserfields.primaryminor = secondaryminor
                elif userquery.extrauserfields.primaryminor == "None":
                    userquery.extrauserfields.primaryminor = secondaryminor
                elif userquery.extrauserfields.primaryminor == "none":
                    userquery.extrauserfields.primaryminor = secondaryminor
                elif userquery.extrauserfields.primaryminor == "NONE":
                    userquery.extrauserfields.primaryminor = secondaryminor
                elif userquery.extrauserfields.primaryminor == None:
                    userquery.extrauserfields.primaryminor = secondaryminor
                else:
                    userquery.extrauserfields.secondaryminor = secondaryminor
                userquery.extrauserfields.save()
                userquery.save()
            if rollnumber != "":
                userquery.extrauserfields.rollnumber = rollnumber
                userquery.extrauserfields.save()
                userquery.save()
            if phonenumber != "":
                userquery.extrauserfields.rollnumber = phonenumber
                userquery.extrauserfields.save()
                userquery.save()
            if rank != "":
                userquery.extrauserfields.rank = rank
                userquery.extrauserfields.save()
                userquery.save()
            rankother = request.POST['other']
            context['userquery'] = userquery
            context['majors'] = userquery.extrauserfields.getMajorsString()
            context['minors'] = userquery.extrauserfields.getMinorsString()
            if userquery == user:
                context['viewingSelf']=True
                context['isAdmin']=True
            return render(request, 'Directory/user.html', context)
        #Deletion of a user via a POST request
        if request.method == 'POST' and 'delete_user' in request.POST:
            username = request.POST['username']
            User.objects.filter(username=username).delete()
            return redirect('/Directory')
        #get sorted list of all users matching the searchterms
        if request.method == 'POST' and 'Search' in request.POST:
            searchterms = [x.strip() for x in str(request.POST['searchterm']).split(" ")]
            userlist = []
            for term in searchterms:
                userlist.extend(User.objects.filter(username=term))
                userlist.extend(User.objects.filter(first_name=term))
                userlist.extend(User.objects.filter(last_name=term))
            userset = set(userlist)
            userlist = list(userset)
            context['userlist'] = sorted(
                userlist, 
                key=lambda user: user.first_name)
        else:
            context['userlist'] = []
            user_list = User.objects.all().order_by('first_name')
            for user in user_list:
                if hasattr(user, 'extrauserfields'):
                    context['userlist'].append(user)
        return render(request, 'Directory/index.html', context)
    else:
        return redirect('/?redirected=True')
