from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

#Class for making announcements
class Bulletin(models.Model):
	creator = models.CharField(max_length = 200)#username of user who created the announcement
	title = models.CharField(max_length = 200)
	text = models.TextField(max_length = 200)
	postDate = models.DateTimeField (default = timezone.now, editable = False)
	expiration_date = models.DateField(default=timezone.make_aware(datetime.datetime.now() + datetime.timedelta(days=10)).date())#when to delete object
  
#Orders all queries with the most recently created first
	class Meta:
		ordering = ['-postDate']
  
#Recommended Unicode method
	def __unicode__(self):
		return unicode(self.title)

#Recommended str method
	def __str__(self):
		return self.title

#deletes all expired bulletins once a day
class BulletinClearer(models.Model):
	last_check = models.DateField(default = timezone.make_aware(datetime.datetime.now() - datetime.timedelta(days=10)).date())#last time bulletins were checked
	def Clear_Events(self):
		announcements = Bulletin.objects.all()#get list of all Bulletins
		if self.last_check < timezone.now().date() - datetime.timedelta(days=1):#if last check was over a day ago:
			for a in announcements:
				exp = a.expiration_date
				if exp is not  None and exp < timezone.now().date():#delete if expired
					a.delete()
			self.last_check = timezone.now().date()
	class Meta:
		ordering = ['-last_check']
			
