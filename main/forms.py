from time import timezone
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError
from main.models import *
import os

class ProfileUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'login'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'email'}))
    img = forms.ImageField(label='Avatar', required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter the password'}))
    retype_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':' enter the password again'}))

    def clean_img(self):
        max_size = 4
        img = self.cleaned_data.get('img')
        print img
        if img:
            if img._size > max_size * 1024 * 1024:
                print 'large size'
                raise ValidationError("large size")
            return img
        else:
            print 'empty'
            raise ValidationError('empty img')


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
        user_name = self.cleaned_data.get('username')
        new_email = self.cleaned_data.get('email')
        new_password = self.cleaned_data.get('password')
        check_img = self.cleaned_data.get('img', False)
        name_img = handleUploadedFile(check_img)
        user = User.objects.create_user(user_name, new_email)
        user.set_password(new_password)
        user.save()
        print 'before myuser'
        print check_img
        myuser = MyUser.objects.create(user = user, rate = 0, img = name_img)
        print 'create myuser'
        myuser.save()
        print 'save myuser'
        return user

class singin_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))

class Add_question(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',	'placeholder': 'Details here','rows':'5'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tags'}))

    def clean_title(self):
        print ('title 0')
        if self.cleaned_data.get('title'):
            print ('title')
            raise ValidationError('empty title')

    def clean_content(self):
        if self.cleaned_data.get('content'):
            print ('content')
            raise ValidationError('empty content')

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags = tags.split(', ')
        if len(tags) < 3:
            raise ValidationError('Need more tags')

    def save(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        tags = self.cleaned_data.get('tags')
        tags = tags.split(', ')
        user = self.request.user
        q = Question.objects.create(title = title, question_text = content,user = user, pubDate = timezone.now())
        for i in tags:
            try:
                tag = Tags.objects.get(tag = i)
            except Tags.DoesNotExist, a:
                tag = Tags.objects.create(tag = i)
            print i
            q.tags_set.add(tag)

def handleUploadedFile(f):
	# Generate random name
	new_filename = "%s.%s" % (User.objects.make_random_password(10), f.name.split('.')[-1])

	filename = os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + new_filename
	with open(filename, 'wb') as destination:
		destination.write(f.read())
	return new_filename