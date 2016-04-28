from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.core.mail import send_mail
from models import *    
from django.core.mail import send_mail

# Create your views here.


def is_owner(username):
    '''Allows users to limit who can remove supplies from the supply list'''
    admingroups = ["All"]
    adminusers = []

    user = User.objects.filter(username=username)
    if not user.exists():
        return False
    user = user[0]
    if username in adminusers:
        return True
    for group in admingroups:
        group_model = Group.objects.filter(name=group)
        if group_model.exists():
            group_model = group_model[0]
            if group_model in user.groups.all():
                return True
    return False

def index(request):
    '''Handles the creation, deletion, and modification of tasks and supplies'''
    #check if user is logged in and redirect them to index if they're not
    if request.user.is_authenticated():
        user = request.user
        gentasks = []
        ownedtasks = []
        personaltasks = []
        #check each task for ownership
        for task in Task.objects.all():
            if task.incomplete is False and task.creator == user.username:
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
                    i = i+1
                if done is False and task.creator == user.username:
                    ownedtasks.append(task)
        userlist=[x for x in User.objects.all() if x.first_name != "" and x.last_name != ""]
        context = {
            'username':user.username,
            'firstname':user.first_name,
            'lastname':user.last_name,
            'userlist':userlist,
            'usergroups':Group.objects.all(),
            'gentasks':gentasks,
            'personaltasks':personaltasks,
            'ownedtasks':ownedtasks,
            'supplylist':Supply.objects.all(),
            'canEdit':is_owner(user.username)
        }
        if request.method == 'GET' and ('invalidInc' in request.GET or 'invalidDec' in request.GET):
            context['invalidsup'] = "Quantity needs to be a positive number."
        if request.method == 'GET' and 'InvalidSupplyName' in request.GET:
            context['invalidsupplyname'] = "Supply not in the supply list"
        if request.method == 'GET' and 'noUserTask' in request.GET:
            context['invalidtaskassignment'] = "You need to select a group(s) and/or a user(s)"
        if request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/')

        if request.method == 'POST' and 'deletetask' in request.POST:
            task = Task.objects.filter(id=int(request.POST['task_id']))[0]
            if task.creator == user.username:
                task.delete()
            else:
                task.incomplete = False
                task.save()
            return redirect('/Tasks/')
            
        if request.method == 'POST' and 'submittask' in request.POST:
            tasktext = request.POST['task']
            usergroups = request.POST.getlist('usergroups')
            usernames = request.POST.getlist('usernames')
            if usergroups == [] and usernames == []:
                return redirect('/Tasks/?noUserTask=True')
            task = None
            tlist = Task.objects.filter(text=tasktext)
            taskexists = tlist.exists()
            #if the task already exists,simply update the existing one
            if taskexists:
                task = tlist[0]
                grouplist = [g.name for g in task.userlists.all()]
                userlist = [u.username for u in task.users.all()]
                for group in usergroups:
                    if group not in grouplist:
                        grouplist.append(group)
                        group_model = Group.objects.get(name=group)
                        task.userlists.add(group_model)
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
            #create task if it doesn't already exist
            else:
                task = Task.objects.create(creator=user.username, text=tasktext)
                task.save()
                for group in usergroups:
                    new_group = Group.objects.get(name=group)
                    task.userlists.add(new_group)
                for user in usernames:
                    user_model = User.objects.get(username=user)
                    send_mail('New Task', 
                              'A new task has been assigned to you by a fraternity member.',
                              'fratapprpi@gmail.com', [user_model.email], fail_silently=False)
                    task.users.add(user_model)
            #save the new or modified task
            task.save()
            return redirect('/Tasks/')
        if request.method == 'POST' and 'submitsupply' in request.POST:
            supplyname = request.POST['supply']
            quantity = request.POST['quantity']
            if int(quantity) <= 0:
                return redirect('/Tasks/?invalidInc=True')
            supply = None
            slist = Supply.objects.filter(name=supplyname)
            supplyexists = slist.exists()
            #if the supply already exists,simply update the existing one
            if supplyexists:
                supply = slist[0]
                supply.quantity = supply.quantity+int(quantity)
                supply.save()
            #create supply if it doesn't already exist
            else:
                supply = Supply.objects.create(name=supplyname,quantity=quantity)
                supply.save()
            #save supply
            supply.save()
            return redirect('/Tasks/')
        if request.method == 'POST' and 'removesupply' in request.POST:
            supplyname = request.POST['supply']
            quantity = request.POST['quantity']
            if quantity <= 0:
                return redirect('/Tasks/?invalidDec=True')
            supply = None
            slist = Supply.objects.filter(name=supplyname)
            supplyexists = slist.exists()
            #if the supply already exists,simply update the existing one
            if supplyexists:
                supply = slist[0]
                supply.quantity = supply.quantity-int(quantity)
                if supply.quantity <= 0:
                    supply.delete()
                    return redirect('/Tasks/')
                supply.save()
            #create supply if it doesn't already exist
            else:
                return redirect('/Tasks/?InvalidSupplyName=True')
            #save supply
            supply.save()
            return redirect('/Tasks/')
        return render(request, 'Tasks/index.html', context)
    else:
        return redirect('/?redirected=True')
