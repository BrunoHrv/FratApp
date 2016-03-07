from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import os
from os.path import abspath, dirname, join, normpath
from sys import path

SITE_ROOT_tmp = dirname(dirname(abspath(__file__)))
SITE_ROOT = SITE_ROOT_tmp[1:]

TEMPLATE_DIR = normpath('Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')
#TEMPLATE_DIR = normpath('C:/Users/jacobn2/Dropbox/SoftDevD/FratApp/FratApp/FratApp/FratApp/templates')#normpath(join(SITE_ROOT, 'FratApp/templates'))

def index(request):
    ind = normpath(join(TEMPLATE_DIR, 'index.html'))
    return render(request, 'index.html', {})
    #return render(request, 'index.html', {})
#HttpResponse("Hello, world. You're at the main index.")
