from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from models import *

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		user = request.user
		context={
			'username':user.username,
			'firstname':user.first_name,
			'lastname':user.last_name,
			'event': None,
			'event_list':Event.objects.all(),
			'attendee_list':None,
		}
		print context
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')

		if request.method == 'POST' and 'create_event' in request.POST:
			event_title = request.POST['title']
			event_text = request.POST['text']
			event_creator = user.username
			event = Event.objects.create(creator=event_creator, title=event_title, text=event_text)
			event.save()
			return redirect('/AttendanceLists/')

		if request.method == 'GET' and request.GET.get('event_id'):
			event_id = request.GET.get('event_id')
			elist = Event.objects.filter(id = event_id)
			if elist.exists():
				print "-----------------------"
				context['event'] = Event.objects.get(id=event_id)
				context['attendee_list'] = Attendee.objects.filter(event = context['event'])
				context['event_list'] = None
		if request.method == 'POST' and 'add_attendee' in request.POST:
			event_id = request.POST['event_id']
			elist = Event.objects.filter(id = event_id)
			if elist.exists():
				attendee = Attendee.objects.create(name=request.POST['name'], event = Event.objects.get(id=event_id))
				attendee.save()
				return redirect('/AttendanceLists/?event_id=%s' % (event_id) ) 
		return render(request, 'AttendanceLists/index.html', context)
	else:
		return redirect('/?redirected=True')
