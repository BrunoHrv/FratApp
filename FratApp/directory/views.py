from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout

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
				return render(request, 'Directory/user.html', context)
		#get list of all users
		context['userlist']=User.objects.all().order_by('first_name')
		#Logs out if requested, directs to main page if 'POST'
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		return render(request, 'Directory/index.html', context)
	else:
		return redirect('/?redirected=True')
