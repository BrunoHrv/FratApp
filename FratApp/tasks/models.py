from __future__ import unicode_literals
from django.contrib.auth.models import User, Group

import uuid
from django.db import models

# Create your models here.

class Task(models.Model):
	id=models.AutoField(primary_key=True)
	creator=models.CharField(max_length=200)#username of the user who made the task
	text=models.CharField(max_length=200)#task description
	userlists=models.ManyToManyField(Group)#groups to assign task to
	users=models.ManyToManyField(User)#individual users for whom the task is set as a personal task
	incomplete = models.BooleanField(default=True)
	def __str__(self):
		return self.text

class Supply(models.Model):
	id=models.AutoField(primary_key=True)
	name=models.CharField(max_length=200)#name of the item
	quantity=models.IntegerField(default=1)#quantity needed
	def __str__(self):
		return self.quantity+" of "+self.name
