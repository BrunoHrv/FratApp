from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

# Create your models here.

#Class for making announcements
class Bulletin(models.Model):
    """Bulletin model for storing data about Bulletins"""
    creator = models.CharField(max_length=200)#username of user who created the announcement
    title = models.CharField(max_length=200)
    text = models.TextField(max_length=200)
    postDate = models.DateTimeField(default=timezone.now, editable=False)
    expiration_date = models.DateField(
        default=timezone.make_aware(
            datetime.datetime.now() + datetime.timedelta(days=10)).date())#when to delete object
  
#Orders all queries with the most recently created first
    class Meta:
        """Defines the ordering of the Bulletins"""
        ordering = ['-postDate']
  
#Recommended Unicode method
    def __unicode__(self):
        return unicode(self.title)

#Recommended str method
    def __str__(self):
        return self.title


class BulletinClearer(models.Model):
    """Deletes all expired bulletins once a day"""
    #last time bulletins were checked
    last_check = models.DateField(
        default=timezone.make_aware(
            datetime.datetime.now() - datetime.timedelta(days=10)).date())


    def clear_bulletins(self):
        '''Clear all bulletins whose expiration date has passed'''
        announcements = Bulletin.objects.all()
        #if last check was over a day ago:
        compare_date = timezone.now().date() - datetime.timedelta(days=1)
        if self.last_check < compare_date:
            for bulletin in announcements:
                exp = bulletin.expiration_date
                if exp is not  None and exp < timezone.now().date():#delete if expired
                    bulletin.delete()
            self.last_check = timezone.now().date()

    class Meta:
        """Defines ordering of the stored Bulletin Clearers"""
        ordering = ['-last_check']
            
