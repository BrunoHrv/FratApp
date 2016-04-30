from __future__ import unicode_literals
from django.contrib.auth.models import User, Group

import uuid
from django.db import models

# Create your models here.

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    #username of the user who made the task
    creator = models.CharField(max_length=200)
    #task description
    text = models.CharField(max_length=200)
    #groups to assign task to
    userlists = models.ManyToManyField(Group)
    #individual users for whom the task is set as a personal task
    users = models.ManyToManyField(User)
    incomplete = models.BooleanField(default=True)
    def __str__(self):
        return self.text

class Supply(models.Model):
    id = models.AutoField(primary_key=True)
    #name of the item
    name = models.CharField(max_length=200)
    #quantity needed
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.quantity + " of " + self.name
