from __future__ import unicode_literals

from django.db import models

# Create your models here.

#Class for making announcements
class Announcement(models.model):
  creator = models.CharField(Max_Length = 200)
  title = models.CharField(Max_Length = 200)
  text = models.TextField(Max_Length = 200)
  postDate = models.DateTimeField (default = datetime.now, editable = False)
  
  #Orders all queries with the most recently created first
  class Meta:
    ordering = ('-postDate')
  
  #Recommended Unicode method
  def __unicode__(self):
       return unicode(self.title)
