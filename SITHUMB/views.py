from django.shortcuts import render

# Create your views here.

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.contrib.auth.models import *
from SITHUMB import models
from .models import *
from SITHUMB.token_module import get_token, out_token
from SITHUMB.authentication_module import TokenAuth2

import redis
import json
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

cur_activity_id = 1


def index(request):
    return render(request, "index.html")


def activityAdd(request):
    return render(request, "system_activityAdd.html")


class AuthAdminLogin(APIView):
    @csrf_exempt
    def post(self, request):
        response = {"status": 100, "msg": None}
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token = get_token(username, 600)
            # cache.set(username, token, 600)
            response["msg"] = "登录成功"
            response["token"] = token
            response["username"] = username
        else:
            response["msg"] = "用户名或密码错误"
        return Response(response)


class LoginTest(APIView):
    authentication_classes = [TokenAuth2]

    def get(self, request):
        response = {"status": 100, "msg": None}
        response["msg"] = "已经登录了"
        return Response(response)


class GetFormTest(APIView):
    def get(self, request):
        response = {"status": 100, "form": None}
        response["form"] = {
            "name": "清华军乐2019-2020春季学期招新报名表",
            "date": "2020/03/03-2020/03/05",
            "questions": [
                {
                    "name": "姓名",
                    "type": "Blank"
                },
                {
                    "name": "性别",
                    "type": "Choice",
                    "Choices": [
                        {"choice": "男"},
                        {"choice": "女"}
                    ]
                }
            ]
        }
        return Response(response)


class CreateActivity(APIView):
    def post(self, request):
        name = request.GET.get('name')
        from_date = parse_date(request.GET.get('from'))
        to_date = parse_date(request.GET.get('to'))
        activity = Activity(name=name, from_date=from_date, to_date=to_date)
        activity.save()
        response = {"status": 100, "a_id": activity.id}
        return Response(response)


class CreateRegisterForm(APIView):
    def post(self, request, id):
        activity_id = id
        application_format = json.dumps(request.data)
        print(application_format)
        activity = Activity.objects.get(id=activity_id)
        activity.application_format = application_format
        activity.save()
        response = {"status": 100, "msg": None}
        return Response(response)


class CreateExaminer(APIView):
    def post(self, request, id):
        activity_id = id
        username = request.GET.get('username')
        password = request.GET.get('password')
        print(activity_id, username, password)
        examiner = User(username=username, password=make_password(password))
        examiner.save()
        examiner.extension.activity = Activity.objects.get(id=activity_id)
        examiner.extension.save()
        examiner.save()
        response = {"status": 100, "msg": None}
        return Response(response)


class CreateSection(APIView):
    def post(self, request, id):
        activity_id = id
        name = request.GET.get('name')
        ac = Activity.objects.get(id=activity_id)
        section = Section(a_id=activity_id, s_id=ac.section_cnt, name=name)
        section.save()
        ac.section_cnt += 1
        ac.save()
        section.activity = ac
        section.save()
        response = {"status": 100, "msg": None}
        return Response(response)


class AddExaminer(APIView):
    def post(self, request, id, sectionID):
        activity_id = id
        section_id = sectionID
        username = request.GET.get('username')
        print(activity_id, section_id, username)
        examiner = User.objects.get(username=username).extension
        examiner.save()
        examiner.sections.add(Section.objects.get(s_id=section_id, a_id=activity_id))
        response = {"status": 100, "msg": None}
        return Response(response)


class CreateForm(APIView):
    def post(self, request, id, sectionID):
        activity_id = id
        section_id = sectionID
        transcript_format = json.dumps(request.data)
        activity = Activity.objects.get(id=activity_id)
        section = Section.objects.get(s_id=section_id, activity=activity)
        section.transcript_format = transcript_format
        section.save()
        response = {"status": 100, "msg": None}
        return Response(response)


class GetActivityList(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "activities": []}
        num = Activity.objects.count()
        if num == 0:
            res = Response()
            res.status_code = 404
            return res
        else:
            data = Activity.objects.all()
            for obj in data:
                json_obj = {
                    "id": obj.id,
                    "name": obj.name,
                    "from": obj.from_date,
                    "to": obj.to_date
                }
                response["activities"].append(json_obj)
            return Response(response)


class GetActivityDetail(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "form": None, "sections": []}
        activity_id = request.GET.get('id')
        activity = Activity.objects.get(id=activity_id)
        if activity is None:
            res = Response()
            res.status_code = 404
            return res
        response["form"] = activity.application_format
        section_list = Section.objects.filter(a_id=activity_id)
        if len(section_list) > 0:
            for obj in section_list:
                json_obj = {
                    "id": obj.s_id,
                    "name": obj.name,
                }
                response["sections"].append(json_obj)
        return Response(response)


class GetSection(APIView):
    def get(self, request):
        # response = {"status": 100, "msg": None, "form": None, "sections": []}
        activity_id = request.GET.get('activityID')
        section_id = request.GET.get('sectionID')
        section = Section.objects.get(a_id=activity_id, s_id=section_id)

        if section is None:
            res = Response()
            res.status_code = 404
            return res
        else:
            name = section.name
            transcript_format = json.loads(section.transcript_format)
            return Response({"name": name, "form": transcript_format})

        # return Response(response)


class GetExaminers(APIView):
    def get(self, request):
        # response = {"status": 100, "msg": None, "form": None, "sections": []}
        activity_id = request.GET.get('activityID')

        activity = Activity.objects.get(id=activity_id)

        if activity is None:
            res = Response()
            res.status_code = 404
            return res
        else:
            examiners = activity.examiners.all()
            examiners_info = []
            for e in examiners:
                sections = e.sections.all()

                sections_info = []
                for s in sections:
                    sections_info.append({"name": s.name})
                examiners_info.append({"username": e.user.username,
                                       "sections": sections_info})
            return Response({"examiners": examiners_info})

        # return Response(response)


class Register(APIView):
    def post(self, request):
        wx_id = request.GET.get('wxID')
        candidates = Candidate.objects.filter(wx_id=wx_id)

        if len(candidates) == 0:
            Candidate.objects.create(wx_id=wx_id)
            response = {"status": 100, "msg": None}
        else:
            response = {"status": 400, "msg": "Already exist"}

        return Response(response)


class ApplicationForm(APIView):
    def post(self, request):
        wx_id = request.GET.get('wxID')
        candidate = Candidate.objects.get(wx_id=wx_id)
        application_form = json.dumps(request.data)
        activity = Activity.objects.get(id=cur_activity_id)
        try:
            application = candidate.applications.get(a_id=cur_activity_id)
        except:
            application = Application(a_id=cur_activity_id, candidate=candidate,
                                      application_form=application_form, activity=activity)
            application.save()
        else:
            application.application_form = application_form
            application.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def get(self, request):
        wx_id = request.GET.get('wxID')
        a_id = request.GET.get('activityID')
        candidate = Candidate.objects.get(wx_id=wx_id)
        response = json.loads(candidate.applications.get(a_id=cur_activity_id).application_form)
        return Response(response)


class Status(APIView):
    def get(self, request):
        wx_id = request.GET.get('wxID')
        candidate = Candidate.objects.get(wx_id=wx_id)
        stage = candidate.applications.get(a_id=cur_activity_id).stage
        section = Section.objects.get(a_id=cur_activity_id, s_id=stage)

        response = {"status": "您的下一步是" + section.name + "请在" + section.address + "等待"}
        return Response(response)


class AuthExaminerLogin(APIView):
    @csrf_exempt
    def post(self, request):
        response = {"status": 100, "msg": None}
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token = get_token(username, 600)
            # cache.set(username, token, 600)
            response["msg"] = "登录成功"
            response["token"] = token
            response["username"] = username
        else:
            response["msg"] = "用户名或密码错误"
        return Response(response)


class GetSection_Examiner(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "sections": []}
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        examiner = Examiner.objects.get(user=user)
        for sec in examiner.sections.all():
            jsonobj = {
                "s_ID": sec.s_id,
                "name": sec.name
            }
            response["sections"].append(jsonobj)
        return Response(response)

class GetCandidateList_Examiner(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "candidates": []}
        s_id = request.GET.get('s_ID')
        candidate_list = Application.objects.filter(stage=s_id)
        for candidate in candidate_list:
            jsonobj = {
                "name": candidate.name,
                "ID": candidate.ID,
                "wxID": candidate.wx_id
            }
            response["candidates"].append(jsonobj)
        return Response(response)

class Transcript(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "application": None, "transcript": None}
        wxID = request.GET.get("wxID")
        candidate = Application.objects.get(wxID=wxID, activity=cur_activity_id)
        response["application"] = json.loads(candidate.application_form)
        response["transcript"] = json.loads(candidate.transcript)
        return Response(response)

    def post(self, request):
        response = {"status": 100, "msg": None}
        wxID = request.GET.get("wxID")
        s_ID = request.GET.get("s_ID")
        candidate = Application.objects.get(wxID=wxID, activity=cur_activity_id)
        transcrpit = json.loads(candidate.transcript)["sections"]
        for sec in transcrpit:
            if sec["s_ID"] == s_ID:
                sec["form"] = request.body
                break
        return Response(response)