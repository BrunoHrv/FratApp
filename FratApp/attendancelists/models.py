from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Class for Attendees for attendance lists
class Attendee (models.Model):
  firstName = models.CharField(max_length = 25)
  lastName = models.CharField(max_length = 25)
  affiliation = models.CharField(max_length = 25)
  
  #Orders all queries by last name
  class Meta:
    ordering = ('lastName')
    
  def __unicode__(self):
    return unicode(self.lastName)
