from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator
from main.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import datetime
from random import randrange
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import *
from django.utils import timezone

def getQuestion(request):
    if request.GET.get("tag"):
        tag = Tags.objects.filter(tag = request.GET.get("tag")).first()
        if tag is None:
            question = Question.objects.order_by('-pubDate')
        else:
            question = tag.question.order_by('-pubDate')
    else:
        question = Question.objects.order_by('-pubDate')
    return question

def main(request):
    question = getQuestion(request)
    q = Paginator(question,10)
    num_page = request.GET.get('page')
    if request.user.is_authenticated():
        prof = MyUser.objects.get(user_id=request.user.id)
    else:
        prof = ""
    try:
        page = q.page(num_page)
    except PageNotAnInteger:
        page = q.page(1)
        num_page = 1
    except EmptyPage:
        page = q.page(q.num_pages)
        num_page = q.num_pages
    for quest in page:
        quest.count = quest.answer_set.count()
        quest.tags = quest.tags_set.all()
        if prof != "":
            like = Like.objects.filter(question = quest, author  = prof)
            if like.exists():
                quest.voice = 0
            else:
                quest.voice = 1
        else:
            quest.voice = 1

    tag = Tags.objects.all()[:10]
    members = MyUser.objects.select_related("user").all().order_by('-rate')[:10]

    # print members.user.username

    k = []
    for i in range(int(num_page)-4, int(num_page)+4):
        if i in q.page_range:
            k.append(i)
    user = request.user
    context = {
        "profile": prof,
        "questions":  page,
        "paginators": k,
        "all_pages": q.num_pages,
        "mytag": tag,
        "bastMemb": members,
    }
    return render(request, 'main/content.html', context)

def user(request):
    if request.user.is_authenticated():
        prof = MyUser.objects.get(user_id=request.user.id)
    else:
        prof = ""
    this_user = MyUser.objects.get(user_id=request.GET.get("user"))
    tag = Tags.objects.all()[:10]
    members = MyUser.objects.select_related("user").all().order_by('-rate')[:10]
    context = {
        "profile": prof,
        "this": this_user,
        "mytag": tag,
        "bastMemb": members,
    }
    print prof
    return render(request, 'main/user.html', context)

@login_required(login_url='/signin/')
def ask(request):
    form = Add_question()
    return render(request, 'main/ask.html', {'form': form})

def add(request):
    if request.user.is_authenticated:
        print 0
        if request.POST:
            print 1
            form = Add_question(request.POST)
            if form.is_valid():
                print 'point1'
                title = form.cleaned_data.get('title')
                content = form.cleaned_data.get('content')
                tags = form.cleaned_data.get('tags')
                tags = tags.split(', ')
                user = request.user
                q = Question.objects.create(title = title, question_text = content,user = user, pubDate = timezone.now())
                print 'point2 '+q.title

                for i in tags:
                    try:
                        tag = Tags.objects.get(tag = i)
                    except Tags.DoesNotExist, a:
                        tag = Tags.objects.create(tag = i)
                    print i
                    q.tags_set.add(tag)
                return redirect('/')
            else:
                print 3
                return render(request, 'main/ask.html', {'form':form})
        else:
            form = Add_question()
            print 4
            return render(request, 'main/ask.html', {'form' : form})

def question(request, quest):
    num_page = request.GET.get('page')

    question = Question.objects.all().get(id=int(quest))

    answers = question.answer_set.all()
    # answers = Answer.objects.all().filter(question = int(quest))
    p = Paginator(answers, 5)
    try:
        page = p.page(num_page)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(p.num_pages)

    if request.user.is_authenticated():
        prof = MyUser.objects.get(user_id=request.user.id);
    else:
        prof = ""

    tag = Tags.objects.all()[:10]
    members = MyUser.objects.select_related("user").all().order_by('-rate')[:10]

    context = {
        "question": question,
        "count": question.answer_set.count(),
        "tags": question.tags_set.all(),
        "answers" : page,
        "profile" : prof,
        "likes" : question.like_set.count(),
        "mytag": tag,
        "bastMemb": members,
    }

    if context["question"]:
        return render(request, 'main/question.html', context)
    else:
        return render(request, 'main/question.html')

def register(request):
    return render(request, 'main/register.html')

def signin(request):
    return render(request, 'main/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

# def login(request):
#     if request.POST:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return HttpResponse('ok', imetype='text/html')
#         else:
#             return HttpResponse('bad Password!', mimetype='text/html')
#             #return render(request)
#     else:
#         return HttpResponse('error', mimetype="text/html")

def login(request):
    if not request.user.is_authenticated():
        form = singin_form();
        if request.POST:
            form = singin_form(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    # url = request.POST.get('next')
                    # print url
                    return HttpResponseRedirect('/')
            return render(request,'main/login.html', {'form':form, 'bad_user':True})
    else:
        return redirect('/')

def signup(request):
    form = ProfileUser()
    print('point1')
    if request.POST:
        form = ProfileUser(request.POST)
        if form.is_valid():
            print('point2')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get("email")
            u = User.objects.create(username=username, email = email)
            u.set_password(password)
            u.save()
            m = MyUser.objects.create(user = u, rate = 0)
            return redirect('/')
        else:
            print('point3')
            return render(request, 'main/register.html', {'form': form})
    print('point4')
    return render(request, 'main/register.html', {'form': form})