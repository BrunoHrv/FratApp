from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.core.mail import send_mail
from models import *    

# Create your views here.

admingroups=["All"]
adminusers=[]

def isOwner(username):#optional; allows users to limit who can remove supplies from the supply list
    user = User.objects.filter(username=username)
    if not user.exists():
        return False
    user=user[0]
    if username in adminusers:
        return True
    for group in admingroups:
        g = Group.objects.filter(name=group)
        if g.exists():
            g=g[0]
            if g in user.groups.all():
                return True
    return False

def index(request):
    if request.user.is_authenticated():#check if user is logged in and redirect them to index if they're not
        user = request.user
        gentasks = []
        ownedtasks=[]
        personaltasks=[]
        for task in Task.objects.all():#check each task
            if task.incomplete == False and task.creator==user.username:
                ownedtasks.append(task)
            if user in task.users.all():#if the user is mentioned by name, it is a personal task
                personaltasks.append(task)
            else:#if the user is in a group that was assigned the task, it is a general task
                done = False
                i = 0
                ngroups = len(task.userlists.all())
                while not done and i < ngroups:
                    group = task.userlists.all()[i]
                    if group in user.groups.all():
                        gentasks.append(task)
                        done = True
                    i =i+1
                if done == False and task.creator==user.username:
                    ownedtasks.append(task)
        userlist=[x for x in User.objects.all() if x.first_name != "" and x.last_name != ""]
        context={
            'username':user.username,
            'firstname':user.first_name,
            'lastname':user.last_name,
            'userlist':userlist,
            'usergroups':Group.objects.all(),
            'gentasks':gentasks,
            'personaltasks':personaltasks,
            'ownedtasks':ownedtasks,
            'supplylist':Supply.objects.all(),
            'canEdit':isOwner(user.username)
        }
        if request.method == 'GET' and ('invalidInc' in request.GET or 'invalidDec' in request.GET):
            context['invalidsup']="Quantity needs to be a positive number."
        if request.method == 'GET' and 'InvalidSupplyName' in request.GET:
            context['invalidsupplyname']="Supply not in the supply list"
        if request.method == 'GET' and 'noUserTask' in request.GET:
            context['invalidtaskassignment']="You need to select either a group(s) and/or a user(s)"
        if request.method== 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/')

        if request.method=='POST' and 'deletetask' in request.POST:
            task = Task.objects.filter(id=int(request.POST['task_id']))[0]
            if task.creator == user.username:
                task.delete()
            else:
                task.incomplete=False
                task.save()
            return redirect('/Tasks/')
            
        if request.method=='POST' and 'submittask' in request.POST:
            tasktext=request.POST['task']
            usergroups=request.POST.getlist('usergroups')
            usernames=request.POST.getlist('usernames')
            if usergroups == [] and usernames==[]:
                return redirect('/Tasks/?noUserTask=True')
            task = None
            tlist = Task.objects.filter(text=tasktext)
            taskexists = tlist.exists()
            if taskexists:#if the task already exists,simply update the existing one
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
                        user_model = User.objects.get(username=user)
                        send_mail('New Task', 
                                  'A new task has been assigned to you by a fraternity member.',
                                  'fratapprpi@gmail.com', [user_model.email], fail_silently=False)
                        
                        task.users.add(user_model)
                        task.save()
            else:#create task if it doesn't already exist
                task = Task.objects.create(creator=user.username, text=tasktext)
                task.save()
                for group in usergroups:
                    g = Group.objects.get(name=group)
                    task.userlists.add(g)
                for user in usernames:
                    user_model = User.objects.get(username=user)
                    send_mail('New Task', 
                              'A new task has been assigned to you by a fraternity member.',
                              'fratapprpi@gmail.com', [user_model.email], fail_silently=False)
                    task.users.add(user_model)
            task.save()#save task
            return redirect('/Tasks/')
        if request.method=='POST' and 'submitsupply' in request.POST:
            supplyname=request.POST['supply']
            quantity=request.POST['quantity']
            if int(quantity) <= 0:
                return redirect('/Tasks/?invalidInc=True')
            supply = None
            slist = Supply.objects.filter(name=supplyname)
            supplyexists = slist.exists()
            if supplyexists:#if the supply already exists,simply update the existing one
                supply = slist[0]
                supply.quantity=supply.quantity+int(quantity)
                supply.save()
            else:#create supply if it doesn't already exist
                supply = Supply.objects.create(name=supplyname,quantity=quantity)
                supply.save()
            supply.save()#save supply
            return redirect('/Tasks/')
        if request.method=='POST' and 'removesupply' in request.POST:
            supplyname=request.POST['supply']
            quantity=request.POST['quantity']
            if quantity <= 0:
                return redirect('/Tasks/?invalidDec=True')
            supply = None
            slist = Supply.objects.filter(name=supplyname)
            supplyexists = slist.exists()
            if supplyexists:#if the supply already exists,simply update the existing one
                supply = slist[0]
                supply.quantity=supply.quantity-int(quantity)
                if supply.quantity <= 0:
                    supply.delete()
                    return redirect('/Tasks/')
                supply.save()
            else:#display error if the supply does not exist
                return redirect('/Tasks/?InvalidSupplyName=True')
            supply.save()#save supply
            return redirect('/Tasks/')
        return render(request, 'Tasks/index.html', context)
    else:
        return redirect('/?redirected=True')
