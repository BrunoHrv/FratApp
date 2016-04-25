from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


# Create your models here.

#Class for storing big brother information
class BigBrother(models.Model):
	bigbrother = models.CharField(max_length = 200)#username of big brother
	littlebrother = models.OneToOneField(User,on_delete=models.CASCADE)

#Class for storing each brother's rank
class Rank(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	rank = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.rank

#Class for storing each brother's hometown
class Hometown(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	hometown = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.hometown

#Class for storing each brother's major
class Major(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	primary = models.CharField(max_length = 200)
	secondary = models.CharField(max_length = 200, default="")

	def getMajors(self):
		return [self.primary, self.secondary]
	def __str__(self):
		if self.secondary not in [None, "None", "none", "NONE", ""]:
			return self.primary+", "+self.secondary
		return self.primary

#Class for storing each brother's minor
class Minor(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	primary = models.CharField(max_length = 200)
	secondary = models.CharField(max_length = 200, default="")

	def getMinors(self):
		return [self.primary, self.secondary]
	def __str__(self):
		if self.secondary not in [None, "None", "none", "NONE", ""]:
			return self.primary+", "+self.secondary
		return self.primary

#Class for storing each brother's graduation date
class GradDate(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	graduation_date = models.DateTimeField()
	
	def __str__(self):
		return __str__(self.graduation_date)

#Class for storing each brother's phone number
class PhoneNumber(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	number = models.CharField(max_length = 200)
	
	def __str__(self):
		return self.number

#Class for storing each brother's roll number
class RollNumber(models.Model):
	brother = models.OneToOneField(User,on_delete=models.CASCADE)
	number = models.IntegerField()
	
	def __str__(self):
		return __str__(self.number)
