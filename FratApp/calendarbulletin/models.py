from __future__ import unicode_literals

from django.db import models
from datetime import datetime  

# Create your models here.

#Class for making announcements
class Bulletin(models.Model):
  creator = models.CharField(max_length = 200)
  title = models.CharField(max_length = 200)
  text = models.TextField(max_length = 200)
  postDate = models.DateTimeField (default = datetime.now, editable = False)
  
#Orders all queries with the most recently created first
  class Meta:
    ordering = ['-postDate']
  
  #Recommended Unicode method
  def __unicode__(self):
       return unicode(self.title)
