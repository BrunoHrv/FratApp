from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


# Create your models here.
class ExtraUserFields(models.Model):
    brother = models.OneToOneField(User, on_delete=models.CASCADE)
    rank = models.CharField(max_length=200)
    graduation_date = models.DateField()
    rollnumber = models.IntegerField()
    bigbrother = models.CharField(default="None/Unknown", max_length=200)#optional
    hometown = models.CharField(default="Unknown", max_length=200)#optional
    primarymajor = models.CharField(max_length=200)#required
    secondarymajor = models.CharField(max_length=200, default="")#optional
    primaryminor = models.CharField(max_length=200, default="None")#optional
    secondaryminor = models.CharField(max_length=200, default="")#optional
    phonenumber = models.CharField(max_length=200, default="")#optional

    def getMajors(self):
        return [self.primarymajor, self.secondarymajor]

    def getMajorsString(self):
        if self.secondarymajor not in [None, "None", "none", "NONE", ""]:
            return self.primarymajor+", "+self.secondarymajor
        return self.primarymajor

    def getMinors(self):
        return [self.primaryminor, self.secondaryminor]
        
    def getMinorsString(self):
        if self.secondaryminor not in [None, "None", "none", "NONE", ""]:
            return self.primaryminor+", "+self.secondaryminor
        return self.primaryminor
