from typing import Any, Dict
from django import forms
from . import models

class LoginForm(forms.Form):
    def clean(self):
        cleand_data = super().clean()
        username = cleand_data.get('username')
        password = cleand_data.get('password')

        users = models.User.objects.filter(username = username)
        if not users.exists():
            raise forms.ValidationError(('User or password wrong'), code='invalid')
        
        user = models.User.objects.get(username = username)
        password2 = user.password
        if password != password2:
            raise forms.ValidationError(('User or password wrong'), code='invalid')

    username =  forms.CharField(min_length=3, max_length=16, label='username')
    password = forms.CharField(min_length=8, max_length=16, label='password', widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        list = models.User.objects.filter(username = username)
        if list.exists():
            raise forms.ValidationError(('User already exist'), code='invalid')
        
        if len(username) > 16 or len(username) < 3:
            raise forms.ValidationError(('Username tp short or to long'), code='invalid')


    class Meta:
        model = models.User
        exclude = {'avatar', 'is_private'}
        widgets = {'password': forms.PasswordInput()}
