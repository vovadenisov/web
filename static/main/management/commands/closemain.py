from django.core.management.base import BaseCommand
from django.db import models
from django.contrib.auth.models import User
from main.models import Question, Answer, Like, Tags, MyUser
import random
import datetime
from random import randrange

class Command(BaseCommand):
    args = '<ask_id ask_id ...>'
    '''help = 'Closes the specified poll for voting'''
    def handle(self, *args, **options):
        if args[0] == u'correct':
            self.addMyUser()
        if args[0] == u'create':
            self.create(args[1], args[2])
        else:
            print u"Command not found!"
    def create(self, model, count):
        if model == u"u":
            self.createUser(count)
        elif model == u"q":
            self.createQuestion(count)
        elif model == u"a":
            self.createAnswer(count)
        elif model == u"t":
            self.createTag(count)
        else:
            print u"Not found model!"

    def createUser(self, count):
        for i in range(int(count)):
            name = random.choice([u'Vova',u'Igor',u'Vika',u'Marina',u'Serega',u'Alla', u'Natasha', u'User']) + '_' + str(random.randint(1, 10000))
            eemail = name + u'@' + u'mail.ru'
            ppassword = u'aaa'
            user = User.objects.create_user(username=name, email=eemail, password=ppassword,)
            user.save()
            rating = randrange(0, 1000)
            myuser = MyUser(rate=rating,user=user)
            myuser.save()
            print (u"User created!")

    def addMyUser(self):
        user_list = User.objects.all()
        for user in user_list:
            my_user = MyUser(user = user, rate = randrange(0, 1000))
            my_user.save()

    def createQuestion(self, count):
        for i in range(int(count)):
            now = datetime.datetime.now()
            title = random.choice("qwertyuiolkjhgfdsazxcvbnm") + random.choice("qwertyuiolkjhgfdsazxcvbnm") + random.choice("qwertyuiolkjhgfdsazxcvbnm")
            for i in range(20):
                text = random.choice("qwertyuiolkjhgfdsazxcvbnm") + random.choice("qwertyuiolkjhgfdsazxcvbnm") + random.choice("qwertyuiolkjhgfdsazxcvbnm")
                text = text*5 + "/n"
            i = random.choice(User.objects.all())
            rating = randrange(0, 1000)
            question = Question(title = title, question_text = text, user = i, pubDate = now, rating = rating)
            question.save()
            print ("Question created!")

    def createAnswer(self, count):
        for i in range(int(count)):
            now = datetime.datetime.now()
            for i in "qwertyuiop":
                text = random.choice("qwertyuiolkjhgfdsazxcvbnm") + random.choice("qwertyuiolkjhgfdsazxcvbnm") + random.choice("qwertyuiolkjhgfdsazxcvbnm")
                text = text*5 + "/n"
            i = random.choice(Question.objects.all())
            j = random.choice(User.objects.all())
            an = Answer(question = i,ansText = text, user = j,pubDate = now)
            an.save()
            print ("Answer created!")

    def createTag(self, count):
        for i in range(int(count)):
            word  =  i
            t = Tags(tag = word)
            t.save()
            i = random.choice(Question.objects.all())
            i.tags_set.add(t)
            i.save()
            print ("Tag created!")



# class MyUser(models.Model):
#     user = models.OneToOneField(User)
#     rate = models.IntegerField(default=0)
#     def __unicode__(self):
#         return self.user.name
#
# class Question(models.Model):
#     title = models.CharField(max_length=100)
#     question_text = models.CharField(max_length=600)
#     user = models.ForeignKey(MyUser)
#     pubDate = models.DateField('date published')
#     rating = models.IntegerField(default=0)
#     def __unicode__(self):
#         return self.title
#
# class Answer(models.Model):
#     ansText = models.CharField(max_length=600)
#     user = models.ForeignKey(MyUser)
#     question = models.ForeignKey(Question)
#     pubDate = models.DateTimeField('date published')
#     best = models.BooleanField(default='false')
#     rating = models.IntegerField(default=0)
#     def __unicode__(self):
#         return self.ansText