from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError
from main.models import *

class ProfileUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'login'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter the password'}))
    retype_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':' enter the password again'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email = email)
            raise ValidationError('Email already in use')
        except User.DoesNotExist, a:
            pass

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username = username)
            raise ValidationError('Username already in use')
        except User.DoesNotExist, a:
            pass

        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        repeatPass = self.cleaned_data.get('retype_pass')
        if password != repeatPass:
            self.add_error('password', 'the passwords do not match')
            self.add_error('retype_pass', 'the passwords do not match')
            raise ValidationError('incorrect password')

    def save(self):
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		u = User.objects.create_user(username, email, password)
		m = MyUser.objects.create(user = u, rate = 0)

class singin_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))

class Add_question(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',	'placeholder': 'Details here','rows':'5'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tags'}))

    def cleaned_title(self):
        print ('title 0')
        if self.cleaned_data.get('title') == '':
            print ('title')
            raise ValidationError('empty title')

    def cleaned_content(self):
        if self.cleaned_data.get('content') == '':
            print ('content')
            raise ValidationError('empty content')

    def cleaned_tags(self):
        tags = self.cleaned_data.get('tags')
        tags = tags.split(', ')
        print tags
        print tags.__len__()
        if tags.__len__() < 3:
            print ('tags')
            raise ValidationError('Need more tags')