from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _
from customauth.models import FratAppUser


#Form for creating new users
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget = forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget = forms.PasswordInput
    
    class Meta:
        model = FratAppUser
        fields = ('email', 'firstName', 'lastName')
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
        
    def save(self, commit=True):
        #saves the provided password in hashed format
        user = super(UserCreationForm,self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user

#updating user form            
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = FratAppUser
        fields = ('email', 'firstName', 'lastName', 'title', 'hometown', 'major', 'rollNumber',
                  'graduationYear', 'phoneNumber', 'isOfficer', 'isAdmin')
        
        def clean_password(self)
            return self.initial["password"]
            
class FratAppAdmin(UserAdmin):
    # The forms to add and change user instances
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('firstName', 'lastName', 'hometown', 'major', 'rollNumber', 'graduationYear', 'phoneNumber')}),
        (_('Permissions'), {'fields': ('isOfficer', 'isAdmin')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'firstName', 'lastName', 'isOfficer', 'isAdmin')
    search_fields = ('email', 'first_name', 'last_name', 'rollNumber')
    ordering = ('lastName',)

admin.site.register(FratAppUser, FratAppAdmin)
        
