from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone

#admins with control over everything
globaladmingroups=['All']
globaladminusers=[]
#admins with control over attendance lists
attendanceadmingroups=[]
attendanceadminusers=[]
attendanceadmingroups.extend(globaladmingroups)
attendanceadminusers.extend(globaladminusers)
#admins with control over the bulletin board
bulletinadmingroups=[]
bulletinadminusers=[]
bulletinadmingroups.extend(globaladmingroups)
bulletinadminusers.extend(globaladminusers)
#admins with control over users
useradmingroups=[]
useradminusers=[]
useradmingroups.extend(globaladmingroups)
useradminusers.extend(globaladminusers)
#admins with control over tasks
taskadmingroups=[]
taskadminusers=[]
taskadmingroups.extend(globaladmingroups)
taskadminusers.extend(globaladminusers)
#admins with control over the supplylist
supplyadmingroups=[]
supplyadminusers=[]
supplyadmingroups.extend(globaladmingroups)
supplyadminusers.extend(globaladminusers)

admindict={}
admindict['global']=[globaladmingroups,globaladminusers]
admindict['attendance']=[attendanceadmingroups,attendanceadminusers]
admindict['bulletin']=[bulletinadmingroups,bulletinadminusers]
admindict['user']=[useradmingroups,useradminusers]
admindict['task']=[taskadmingroups,taskadminusers]
admindict['supply']=[supplyadmingroups,supplyadminusers]

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

    def getAdminPermissions(self,feature='global'):
        if admindict.has_key(feature):
            admingroups=admindict[feature]
            adminusers=admingroups[1]
            admingroups=admingroups[0]
            user=self.brother
            if user.username in adminusers:
                return True
            for group in admingroups:
                group_model = Group.objects.filter(name=group)
                if group_model.exists():
                    group_model = group_model[0]
                    if group_model in user.groups.all():
                        return True
        return False
