from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		context={}
		return render(request, 'Directory/index.html', context)
	else:
		return redirect('/', redirected=True)
