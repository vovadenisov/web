from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.template import RequestContext, loader
from django.core.paginator import Paginator
from main.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from forms import *

from django.core.urlresolvers import reverse

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
    if request.GET:
        num_page = request.GET.get('page')
        try:
            page = q.page(num_page)
        except PageNotAnInteger:
            page = q.page(1)
            print 'PageNotAnInteger'
            num_page = 1
        except EmptyPage:
            page = q.page(q.num_pages)
            num_page = q.num_pages
            print 'empty'
            print num_page
    else:
        num_page = 1
        page = q.page(num_page)

    last_page = q.num_pages

    for quest in page:
        quest.count = quest.answer_set.count()
        quest.tags = quest.tags_set.all()
        # if request.user.is_authenticated:
        # like = Like.objects.filter(question = quest)
        #     if like.exists():
        #         quest.voice = 0
        #     else:
        # quest.voice = 1
        # else:
        #     quest.voice = 1

    # print members.user.username

    k = []
    for i in range(int(num_page)-4, int(num_page)+4):
        if i in q.page_range:
            k.append(i)

    if last_page <= 1:
        is_paginator = False
    else:
        is_paginator = True
    context = {
        # "profile": prof,
        'actual_page': num_page,
        'last_page': last_page,
        'questions':  page,
        'paginators': k,
        'all_pages': q.num_pages,
        'is_paginator': is_paginator
    }
    default = get_default_context()
    context.update(default)
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
    default = get_default_context()
    content = {'form': form}
    content.update(default)
    return render(request, 'main/ask.html', content)

def add(request):
    if request.user.is_authenticated:
        default = get_default_context()
        if request.POST:
            form = Add_question(request.POST, request = request or None)
            if form.is_valid():
                form.save()
                return redirect('/')
            else:
                print 3
                return render(request, 'main/ask.html', default.update({'form':form}))
        else:
            form = Add_question()
            print 4
            return render(request, 'main/ask.html', default.update({'form' : form}))

def question(request, quest):
    # if request.POST:
    #     form = answer_form(request.POST)
    #     if form.is_valid():
    #         form.save()
    #     else:
    #
    form = answer_form()
    if request.GET:
        num_page = request.GET.get('page')
    else:
        num_page = 1
    question = get_object_or_404(Question, id=int(quest))

    answers = question.answer_set.all()
    p = Paginator(answers, 5)
    try:
        page = p.page(num_page)
    except PageNotAnInteger:
        page = p.page(1)
        num_page = 1
    except EmptyPage:
        page = p.page(p.num_pages)
        num_page = p.num_pages
    last_page = p.num_pages

    k=[]

    for i in range(int(num_page)-4, int(num_page)+4):
        if i in p.page_range:
            k.append(i)

    if last_page <= 1:
        is_paginator = False
    else:
        is_paginator = True
    context = {
        "question": question,
        "count": question.answer_set.count(),
        "tags": question.tags_set.all(),
        "answers" : page,
        'is_paginator': is_paginator,
        'last-page': last_page,
        'paginator': k,
        "likes": question.like_set.count(),
        'form':form
    }
    default = get_default_context()
    context.update(default)
    if context["question"]:
        return render(request, 'main/question.html', context)
    else:
        return render(request, 'main/question.html', default)

def register(request):
    context = get_default_context()
    return render(request, 'main/register.html', context)

def signin(request):
    context = get_default_context()
    return render(request, 'main/login.html', context)

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
        default = get_default_context()
        form = singin_form()
        context = {
            'form':form,
            'bad_user':True
        }
        context.update(default)
        if request.POST:
            form = singin_form(request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect('/')
            return render(request,'main/login.html', context)
    else:
        return redirect('/')

@login_required(login_url='/signin/')
def correct_Email(request):
    form = correct_Email_form()
    context = {
        'form': form,
        'btn': 'change'
    }
    default = get_default_context()
    context.update(default)
    if request.POST:
        form = correct_Email_form(request.POST, request.FILES, request = request or None)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'main/register.html', context)
    return render(request, 'main/register.html', context)

@login_required(login_url='/signin/')
def correct(request):
    default = get_default_context()
    return render(request, 'main/correct.html', default)


@login_required(login_url='/signin/')
def correct_password(request):
    default = get_default_context()
    form = correct_password_form()
    context = {
        'form': form,
        'btn': 'change'
    }
    context.update(default)
    if request.POST:
        form = correct_password_form(request.POST, request.FILES, request = request or None)
        context['form'] = form
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'main/register.html', context)
    return render(request, 'main/register.html', context)

@login_required(login_url='/signin/')
def correct_img(request):
    default = get_default_context()
    form = correct_img_form()
    context = {
        'form': form,
        'btn': 'change'
    }
    context.update(default)
    if request.POST:
        form = correct_img_form(request.POST, request.FILES, request = request or None)
        context['form']=form
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'main/register.html', context)
    return render(request, 'main/register.html', context)

def signup(request):
    form = ProfileUser()
    context = {
        'form': form,
        'btn': 'Register'
    }
    default = get_default_context()
    context.update(default)
    if request.POST:
        form = ProfileUser(request.POST, request.FILES)
        context['form']=form
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return render(request, 'main/register.html', context)
    return render(request, 'main/register.html', context)

def get_default_context():
    tag = Tags.objects.all()[:10]
    members = MyUser.objects.select_related("user").all().order_by('-rate')[:10]
    default_context = {
        "mytag": tag,
        "bastMemb": members,
    }
    return default_context