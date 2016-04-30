from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from FratApp.models import *

# Create your views here.

def index(request):
    #Checks to see if logged. Sends back to index page if not logged in
    if request.user.is_authenticated():
        user = request.user
        context = {
            'username':user.username,
            'firstname':user.first_name,
            'lastname':user.last_name,
        }
        #Recieve information from hypertext protocol
        if request.method == 'GET':
            if 'user' in request.GET:#get specific user
                userquery = User.objects.get(username=request.GET['user'])
                context['userquery'] = userquery
                context['majors'] = userquery.extrauserfields.getMajorsString()
                context['minors'] = userquery.extrauserfields.getMinorsString()
                return render(request, 'Directory/user.html', context)
        #Logs out if requested, directs to main page if 'POST'
        if request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/')
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
            context['userlist'] = User.objects.all().order_by('first_name')
        return render(request, 'Directory/index.html', context)
    else:
        return redirect('/?redirected=True')
