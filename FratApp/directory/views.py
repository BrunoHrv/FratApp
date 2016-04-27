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
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
		}
		#Recieve information from hypertext protocool
		if request.method == 'GET':#get specific user
			if 'user' in request.GET:
				userquery=User.objects.get(username=request.GET['user'])
				context['userquery']=userquery
				context['majors']=userquery.extrauserfields.getMajorsString()
				context['minors']=userquery.extrauserfields.getMinorsString()
				return render(request, 'Directory/user.html', context)
		#Logs out if requested, directs to main page if 'POST'
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		#get list of all users
		if request.method == 'POST' and 'Search' in request.POST:
			searchterms = [x.strip() for x in str(request.POST['searchterm']).split(" ")]
			userlist=[]
			for term in searchterms:
				userlist.extend(User.objects.filter(username=term))
				userlist.extend(User.objects.filter(first_name=term))
				userlist.extend(User.objects.filter(last_name=term))
			userlist=set(userlist)
			userlist=list(userlist)
			context['userlist']=sorted(userlist, key=lambda user: user.first_name)#userlist.order_by('first_name')
		else:
			context['userlist']=User.objects.all().order_by('first_name')
		return render(request, 'Directory/index.html', context)
	else:
		return redirect('/?redirected=True')
