from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model):
    user = models.OneToOneField(User)
    rate = models.IntegerField(default=0)
    img = models.ImageField(upload_to='/uploads/', default='1.jpg')
    def __unicode__(self):
        return self.user.username

class Question(models.Model):
    title = models.CharField(max_length=100)
    question_text = models.CharField(max_length=600)
    user = models.ForeignKey(User)
    pubDate = models.DateField('date published')
    rating = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    ansText = models.CharField(max_length=600)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    pubDate = models.DateTimeField('date published')
    best = models.BooleanField(default='false')
    rating = models.IntegerField(default=0)
    def __unicode__(self):
        return self.ansText

class Tags(models.Model):
    tag = models.CharField(max_length=32, unique=True)
    question = models.ManyToManyField(Question)
    def __unicode__(self):
        return self.tag

class Like(models.Model):
	author = models.ForeignKey(MyUser)
	question = models.ForeignKey(Question)
	status = models.BooleanField(default=False)