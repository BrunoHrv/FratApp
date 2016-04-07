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
	def __str__(self):
		return self.text
