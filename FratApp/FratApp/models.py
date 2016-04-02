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
  
class FratAppUser(AbstractBaseUser):
  
  email - models.EmailField(_('email address'), max_length = 254, unique = True)
  firstName = models.CharField(_('first name'), max_length = 25)
  lastName = models.CharField(_('last name'), max_length = 25)
  title = models.CharField(_('title'), max_length = 25, blank = True)
  hometown = models.Charfield(_('title'), max_length = 50, blank = True)
  major = models.Charfield(_('major'), max_length = 25, blank = True)
  
  
  

'''
user = # A User object usually obtained from request.
storage = Storage(CredentialsModel, 'id', user, 'credential')
credential = storage.get()
...
storage.put(credential)
'''
