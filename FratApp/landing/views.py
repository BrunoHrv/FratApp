from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout

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
		return render(request, 'LandingPage/index.html', context)
	else:
		return redirect('/?redirected=True')
