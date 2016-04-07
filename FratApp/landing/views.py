from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from models import *	

# Create your views here.

def index(request):
	if request.user.is_authenticated():#load page if user is logged in, redirect to external landing page if not
		user = request.user
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
		}
		print context
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		if request.method == 'POST' and 'signup' in request.POST:
			print'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
			print request.POST
			username=request.POST['usernamesubmit']
			password=request.POST['passwordsubmit']
			email = request.POST['email']
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
				user = User.objects.create_user(username, email, password)
				user.first_name=firstname
				user.last_name=lastname
				user.groups=[allgroup]
				user.save()#save user to database
			context['usercreated']=user_created
		return render(request, 'LandingPage/index.html', context)
	else:
		return redirect('/?redirected=True')
