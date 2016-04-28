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
			'event': None,#individual event being viewed
			'event_list':Event.objects.all(),
			'attendee_list':None,
		}
		
		if request.method== 'POST' and 'logout' in request.POST:
			logout(request)
			return redirect('/')
		#Creating an event via POST HTTP request
		if request.method == 'POST' and 'create_event' in request.POST:
			event_title = request.POST['title']
			event_text = request.POST['text']
			event_date = request.POST['eventdate']
			event_location = request.POST['location']
			event_creator = user.username
			if event_date:
				event = Event.objects.create(creator=event_creator, title=event_title, text=event_text,location=event_location,eventDate=event_date)
			else:
				event = Event.objects.create(creator=event_creator, title=event_title, text=event_text,location=event_location)
			event.save()
			return redirect('/AttendanceLists/')
		#deleting an attendee via POST data
		if request.method == 'POST' and 'delete_attendee' in request.POST:
			Attendee.objects.filter(id=int(request.POST['delete_attendee'])).delete()
			event_id=request.POST["event_id"]
			redirecturl = '/AttendanceLists/?event_id='+event_id
			return redirect(redirecturl)
		#deleting an event via POST data
		if request.method == 'POST' and 'delete_event' in request.POST:
			Event.objects.filter(id=int(request.POST['event_id'])).delete()
			return redirect('/AttendanceLists/')
		#Rendering a specific Event and its list of attendees via POST data
		if request.method == 'GET' and request.GET.get('event_id'):
			event_id = request.GET.get('event_id')
			elist = Event.objects.filter(id = event_id)
			if elist.exists():
				context['event'] = Event.objects.get(id=event_id)
				context['attendee_list'] = Attendee.objects.filter(event = context['event'])
				context['event_list'] = None
		#Adding an attendee to an Event via POST Data, then redirecting into a GET Request with the event id
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
