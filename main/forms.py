from django import forms
from .models import *
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('location', 'age', 'mail')


class CaseInsensitiveUserCreationForm(UserCreationForm):
    def clean(self):
        cleaned_data = super(CaseInsensitiveUserCreationForm, self).clean()
        username = cleaned_data.get('username')
        if username and User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'A user with that username already exists.')
        return cleaned_data

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('number','name')