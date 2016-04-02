from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import baseUserManager
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
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
    rollNumber = models.IntegerField(blank = True)
    graduationYear = models.IntegerField(blank = True)
    phone number = models.CharField(_('phone number'), max_length = 15, blank = True)
    isOfficer = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName','lastName']
  
    def getFullName(self):
        fullName = '%s %s' % (self.firstName, self.lastName)
        return fullName.strip()
    
    def getEmail(self)
        return self.email
    
class CustomUserManager (BaseUserManager):
    
    def _create_user(self, email, password, first_name, last_name, is_officer, is_admin, **extra_fields):
        if not email":
            raise ValueError('Email is required')
        user = self.model (email = email,
                           firstName = first_name, lastName = last_name,
                           isOfficer = is_officer, isAdmin = is_admin,
                           **extra_fields)
        user.set_password (password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        return self._create_user(email, password, first_name, last_name, False, False, **extra_fields)
    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        return self._create_user(email, password, first_name, last_name, True, True, **extra_fields)
