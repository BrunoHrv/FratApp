from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import Storage
from your_project.your_app.models import CredentialsModel

class FlowModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  flow = FlowField()

class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()

'''
user = # A User object usually obtained from request.
storage = Storage(CredentialsModel, 'id', user, 'credential')
credential = storage.get()
...
storage.put(credential)
'''
