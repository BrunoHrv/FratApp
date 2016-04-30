from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import datetime 
from django.utils import timezone

def index(request):
    """Handles the creation and deletion of bulletins"""
    if request.user.is_authenticated():
        user = request.user
        context = {
            'username':user.username,
            'firstname':user.first_name,
            'lastname':user.last_name,
            'isAdmin':user.extrauserfields.getAdminPermissions('bulletin')
        }
        if request.method == 'POST' and 'logout' in request.POST:
            logout(request)
            return redirect('/')
        #Creation of a bulletin via a POST request
        if request.method == 'POST' and 'addbulletin' in request.POST:
            new_creator = user.username
            new_title = request.POST['title']
            new_description = request.POST['description']
            new_expiration = request.POST['expiration']
            announcement = Bulletin.objects.create(creator=new_creator, 
                                                   title=new_title, 
                                                   text=new_description, 
                                                   expiration_date=new_expiration)
        #Deletion of a bulletin via a POST request
        if request.method == 'POST' and 'delete_bulletin' in request.POST:
            bulletin_id = int(request.POST['bulletin_id'])
            Bulletin.objects.filter(id=bulletin_id).delete()
        checks = BulletinClearer.objects.all()
        clearer = None
        #Code to make certain that there is only one BulletinClearer in the database at once
        if len(checks) == 0:
            clearer = BulletinClearer.objects.create()
        else:
            clearer = checks[len(checks)-1]
            for old_clearer in checks:
                if old_clearer != clearer:
                    old_clearer.delete()
        #BulletinClearer checks to see if any bulletins need to be cleared
        clearer.clear_bulletins()
        bulletin_list = Bulletin.objects.all()
        paginator = Paginator(bulletin_list, 10)
        page = request.GET.get('page')
        try:
            bulletins = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            bulletins = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            bulletins = paginator.page(paginator.num_pages)
        context['bulletins'] = bulletins
        return render(request, 'Calendar/index.html', context)
    else:
        return redirect('/?redirected=True')
