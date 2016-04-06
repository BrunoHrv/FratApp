from __future__ import unicode_literals
from django.contrib.auth.models import User, Group

import uuid
from django.db import models

# Create your models here.

class Task(models.Model):
	id=models.AutoField(primary_key=True)
	creator=models.CharField(max_length=200)
	text=models.CharField(max_length=200)
	userlists=models.ManyToManyField(Group)
	users=models.ManyToManyField(User)
	def __str__(self):
		return self.text
