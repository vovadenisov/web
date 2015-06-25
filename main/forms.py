from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError
from main.models import *
import os
from django.contrib.auth.hashers import check_password

class correct_Email_form(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'email'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                user = User.objects.get(email = email)
                raise ValidationError('Email already in use')
            except User.DoesNotExist, a:
                pass
        return email

    def save(self):
        email = self.cleaned_data.get('email')
        user = self.request.user
        if email:
            user.email = email
            user.save()
        else:
            raise ValidationError('Empty Email')
        return user


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(correct_Email_form, self).__init__(*args, **kwargs)

class correct_img_form(forms.Form):
    img = forms.ImageField(label='Avatar', required=False)

    def clean_img(self):
        max_size = 4
        img = self.cleaned_data.get('img')
        if img:
            if img._size > max_size * 1024 * 1024:
                raise ValidationError("large size")
        else:
            raise ValidationError('empty img')
        return img


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(correct_img_form, self).__init__(*args, **kwargs)

    def save(self):
        img = self.cleaned_data.get('img')
        user = self.request.user
        print 'aaa'
        if img:
            print 'bbb'
            name_img = handleUploadedFile(img)
            os.remove(os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + str(user.myuser.img))
            user.myuser.img = name_img
            user.save()
            user.myuser.save()
        return user

class correct_password_form(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter actualy password'}))
    new_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':' enter new password'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(correct_password_form, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = self.request.user
        if not check_password(password, user.password):
            raise ValidationError('incorrect password')
        return password

    def clean_new_pass(self):
        password = self.cleaned_data.get('new_pass')
        if not password:
            raise ('empty password')
        return password


    def save(self):
        new_pass = self.cleaned_data.get('new_pass')
        user = self.request.user
        if new_pass:
            user.set_password(new_pass)
            user.save()
        return user

class ProfileUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'login'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'email'}))
    img = forms.ImageField(label='Avatar', required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter the password'}))
    retype_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':' enter the password again'}))

    def clean_img(self):
        max_size = 4
        img = self.cleaned_data.get('img')
        if img:
            if img._size > max_size * 1024 * 1024:
                raise ValidationError("large size")
            return img
        else:
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
        myuser = MyUser.objects.create(user = user, rate = 0, img = name_img)
        myuser.save()
        return user

class singin_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))

class answer_form(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',	'placeholder': 'Details here','rows':'5'}))

    def clean_content(self):
        answer = self.cleaned_data.get('answer')
        if not answer:
            raise ValidationError('empty content')
        return answer

class Add_question(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',	'placeholder': 'Details here','rows':'5'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tags'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(Add_question, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('empty title')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise ValidationError('empty content')
        return content

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        tags = tags.split(', ')
        if len(tags) < 3:
            raise ValidationError('Need more tags')
        return tags

    def save(self):
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
        tags = self.cleaned_data.get('tags')
        user = self.request.user
        q = Question.objects.create(title = title, question_text = content,user = user, pubDate = timezone.now())
        for i in tags:
            try:
                tag = Tags.objects.get(tag = i)
            except Tags.DoesNotExist, a:
                tag = Tags.objects.create(tag = i)
            q.tags_set.add(tag)
        return q

def handleUploadedFile(f):
	# Generate random name
	new_filename = "%s.%s" % (User.objects.make_random_password(10), f.name.split('.')[-1])
	filename = os.path.dirname(os.path.dirname(__file__)) + '/uploads/' + new_filename
	with open(filename, 'wb') as destination:
		destination.write(f.read())
	return new_filename

