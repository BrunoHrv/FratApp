from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		user = request.user
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
		}
		if request.method == 'GET':
			if 'user' in request.GET:
				userquery=User.objects.get(username=request.GET['user'])
				context['userquery']=userquery
				return render(request, 'Directory/user.html', context)
		context['userlist']=User.objects.all()
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		return render(request, 'Directory/index.html', context)
	else:
		return redirect('/?redirected=True')
