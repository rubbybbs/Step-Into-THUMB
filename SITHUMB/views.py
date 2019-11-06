from django.shortcuts import render

# Create your views here.

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework.response import Response
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.contrib.auth.models import *
from SITHUMB import models
from .models import *
from SITHUMB.token_module import get_token, out_token

import json
from django.core.cache import cache


def login_view(request):
    response = {"status": 100, "msg": None}
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token = get_token(username, 600)
        cache.set(username, token, 600)
        response["msg"] = "登录成功"
        response["token"] = token
        response["username"] = username
    else:
        response["msg"] = "用户名或密码错误"
    return Response(response)



def create_activity_view(request):
    name = request.POST.get('name')
    from_date = parse_date(request.POST.get('from'))
    to_date = parse_date(request.POST.get('to'))
    Activity.objects.create(name=name, from_date=from_date, to_date=to_date)
    # return


def create_registration_form_view(request):
    activity_id = request.GET.get('id')
    application_format = json.dumps(request.body)
    activity = Activity.objects.get(id=activity_id)
    activity.application_format = application_format
    activity.save()


def create_examiner_view(request):
    activity_id = request.GET.get('id')
    username = request.POST.get('username')
    password = request.POST.get('password')
    examiner = User(username=username, password=make_password(password))
    examiner.extension.activity = Activity.objects.get(id=activity_id)
    examiner.extension.save()
    examiner.save()
    # return


def create_section_view(request):
    activity_id = request.GET.get('id')
    name = request.POST.get('name')
    ac = Activity.objects.get(id=activity_id)
    section = Section(s_id=ac.section_cnt, name=name)
    ac.section_cnt += 1
    ac.save()
    section.save()


def add_examiner_view(request):
    activity_id = request.GET.get('id')
    section_id = request.GET.get('sectionID')
    username = request.POST.get('username')
    examiner = User.objects.get(username=username).extension
    activity = Activity.objects.get(id=activity_id)
    examiner.section = Section.objects.get(s_id=section_id, activity=activity)
    examiner.save()


def create_form_view(request):
    activity_id = request.GET.get('id')
    section_id = request.GET.get('sectionID')
    transcript_format = json.dumps(request.body)
    activity = Activity.objects.get(id=activity_id)
    section = Section.objects.get(s_id=section_id, activity=activity)
    section.transcript_format = transcript_format
    section.save()
