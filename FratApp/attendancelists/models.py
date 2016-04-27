from __future__ import unicode_literals

from django.db import models
from datetime import datetime  

# Create your models here.
class Event(models.Model):
	id = models.AutoField(primary_key=True)
	creator = models.CharField(max_length = 200)
  	title = models.CharField(max_length = 200)
  	text = models.TextField(max_length = 200)
  	postDate = models.DateField (auto_now_add=True, editable = False)
	eventDate= models.DateField (null=True,editable = True)
  	location = models.CharField(default="", max_length = 200)

  	#Orders all queries with the most recently created first
  	class Meta:
  	 	ordering = ['-postDate']
  	
  	#Recommended Unicode method
#  	def __unicode__(self):
#  	    return unicode(self.title)

  	def __str__(self):
		return self.title

class Attendee(models.Model):
	#references a specific event and when that event is deleted, deletes itself
	id = models.AutoField(primary_key=True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	name = models.CharField(max_length = 200)

	def __str__(self):
		return self.name
