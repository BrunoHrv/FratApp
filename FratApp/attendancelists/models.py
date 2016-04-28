from __future__ import unicode_literals

from django.db import models
from datetime import datetime  

# Create your models here.
class Event(models.Model):
    """Tracks the Event Data"""
    id = models.AutoField(primary_key=True)
    creator = models.CharField(max_length=200)#username of user that created the event
    title = models.CharField(max_length=200)#name of the event
    text = models.TextField(max_length=200)#Misc. details
    postDate = models.DateField(auto_now_add=True, editable=False)#when the event was created
    eventDate= models.DateField(null=True, editable=True)#when the event happened, optional
    location = models.CharField(default="", max_length=200)#where the event was, optional

    #Orders all queries with the most recently created first
    class Meta:
        ordering = ['-postDate']

    def __str__(self):
        return self.title


class Attendee(models.Model):
    """Tracks Attendees per event"""
    #references a specific event and when that event is deleted, deletes itself
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)#name of attendee

    def __str__(self):
        return self.name
