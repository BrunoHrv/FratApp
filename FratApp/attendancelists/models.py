from __future__ import unicode_literals

from django.db import models
from datetime import datetime  

# Create your models here.
class Event(models.Model):
	id=models.AutoField(primary_key=True)
	creator = models.CharField(max_length = 200)
  	title = models.CharField(max_length = 200)
  	text = models.TextField(max_length = 200)
  	postDate = models.DateField (auto_now_add=True, editable = False)

  	#Orders all queries with the most recently created first
  	class Meta:
  	 	ordering = ['-postDate']
  	
  	#Recommended Unicode method
  	def __unicode__(self):
  	    return unicode(self.title)

class Attendee(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	name = models.CharField(max_length = 200)