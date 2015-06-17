from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.paginator import Paginator
from main.models import Question, MyUser, Like, Tags, Answer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import datetime
from random import randrange
from django.contrib.auth.decorators import login_required

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

def ask(request):
    return render(request, 'main/ask.html')

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

#def register(request):
#    return render(request, 'main/register.html')