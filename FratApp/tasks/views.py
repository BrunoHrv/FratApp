from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from models import *	

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		user = request.user
		gentasks = []
		personaltasks=[]
		for task in Task.objects.all():
			if user in task.users.all():
				personaltasks.append(task.text)
			else:
				done = False
				i = 0
				ngroups = len(task.userlists.all())
				while not done and i < ngroups:
					group = task.userlists.all()[i]
					if group in user.groups.all():
						gentasks.append(task.text)
						done = True
					i =i+1
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
			'userlist':User.objects.all(),
			'usergroups':Group.objects.all(),
			'gentasks':gentasks,
			'personaltasks':personaltasks,
		}
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		if request.method=='POST' and 'submittask' in request.POST:
			tasktext=request.POST['task']
			usergroups=request.POST.getlist('usergroups')
			usernames=request.POST.getlist('usernames')
			task = None
			tlist = Task.objects.filter(text=tasktext)
			taskexists = tlist.exists()
			if taskexists:
				task = tlist[0]
				grouplist = [g.name for g in task.userlists.all()]
				userlist = [u.username for u in task.users.all()]
				for group in usergroups:
					if group not in grouplist:
						grouplist.append(group)
						g = Group.objects.get(name=group)
						task.userlists.add(g)
						task.save()
				for user in usernames:
					if user not in userlist:
						userlist.append(user)
						u = User.objects.get(username=user)
						task.users.add(u)
						task.save()
			else:
				task = Task.objects.create(creator=user.username, text=tasktext)
				task.save()
				for group in usergroups:
					g = Group.objects.get(name=group)
					task.userlists.add(g)
				for user in usernames:
					u = User.objects.get(username=user)
					task.users.add(u)
			task.save()
			return redirect('/Tasks/')
		return render(request, 'Tasks/index.html', context)
	else:
		return redirect('/?redirected=True')
