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
import requests

import redis
import json
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext

cur_activity_id = -1
try:
    cur_activity_id = Activity.objects.get(status=1).id
except Exception:
    pass


def index(request):
    return render(request, "index.html")


def activity(request):
    return render(request, "activity.html")


def application_form(request):
    return render(request, "modify.html")


def application_segment(request):
    return render(request, "segment.html")


def application_account(request):
    return render(request, "accountManage.html")


def application_finalcheck(request):
    return render(request, "finalcheck.html")


def application_detail(request):
    return render(request, "examinerDetail.html")


def application_score(request):
    return render(request, "score.html")


# 管理员相关接口

class AuthAdminLoginView(APIView):
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


class LoginTestView(APIView):
    authentication_classes = [TokenAuth2]

    def get(self, request):
        response = {"status": 100, "msg": None}
        response["msg"] = "已经登录了"
        return Response(response)


class GetFormTestView(APIView):
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


class ActivityListView(APIView):
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
                    "status": obj.status,
                    "name": obj.name,
                    "from": obj.from_date,
                    "to": obj.to_date
                }
                response["activities"].append(json_obj)
            return Response(response)


class ActivityView(APIView):
    def post(self, request):
        name = request.GET.get('name')
        from_date = parse_date(request.GET.get('from'))
        to_date = parse_date(request.GET.get('to'))
        if from_date == None or to_date == None:
            from_date = parse_date("2000-01-01")
            to_date = parse_date("2100-01-01")

        activity = Activity(name=name, from_date=from_date, to_date=to_date)
        activity.save()
        activity.application_format = "{\"id\":"+str(activity.id)+", \"question\": [{\"name\": \"姓名\", \"type\": " \
                                                             "\"Blank\"}, {\"name\": \"学号\", \"type\": \"Blank\"}]} "
        activity.save()
        response = {"status": 100, "a_id": activity.id}
        return Response(response)

    def delete(self, request):
        activity_id = request.GET.get('activityID')
        Activity.objects.filter(id=activity_id).delete()
        response = {"status": 100, "a_id": activity_id}
        return Response(response)


class ActivityStatusView(APIView):
    def get(self, request):
        activity_id = request.GET.get("activityID")
        a = Activity.objects.get(id=activity_id)
        a.status = 1
        a.save()
        response = {"status": 100, "a_id": activity_id}
        return Response(response)

    def post(self, request):
        activity_id = request.GET.get("activityID")
        a = Activity.objects.get(id=activity_id)
        a.status = 2
        a.save()
        response = {"status": 100, "a_id": activity_id}
        return Response(response)


class RegistrationFormView(APIView):
    def post(self, request, id):
        application_format = str(request.data).replace('\'', '"')

        activity = Activity.objects.get(id=id)
        if activity.status != 0:
            return Response({"status": 400})

        activity.application_format = application_format
        activity.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def get(self, request, id):
        activity = Activity.objects.get(id=id)
        if activity.application_format == '':
            return Response({'form': '{"question":[]}'})
        else:
            return Response({'form': activity.application_format})


class ExaminerListView(APIView):
    def get(self, request, id):
        activity = Activity.objects.get(id=id)

        if activity is None:
            res = Response()
            res.status_code = 404
            return res
        else:
            examiners = activity.examiners.all()
            examiners_info = []
            examiners_count = 0
            for e in examiners:
                examiners_count += 1
                sections = e.sections.all()
                sections_info = []
                for s in sections:
                    sections_info.append({"sectionID": s.s_id, "name": s.name})
                examiners_info.append({"username": e.username,
                                       "password": e.user.password,
                                       "sections": sections_info})
            return Response({"code":0,"msg":"", "count": examiners_count, "data": examiners_info})


class ExaminerView(APIView):
    def post(self, request, id):
        username = request.GET.get('username')
        password = request.GET.get('password')
        sections = request.data["sections"]

        examiner = User(username=username, password=password)
        examiner.save()
        examiner.extension.activity = Activity.objects.get(id=id)
        for s_id in sections:
            examiner.extension.sections.add(Section.objects.get(s_id=s_id, a_id=id))
        examiner.extension.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def delete(self, request, id):
        username = request.GET.get("username")
        User.objects.filter(extension__activity__id=id, username=username).delete()
        response = {"status": 100, "msg": None}
        return Response(response)


class SectionListView(APIView):
    def get(self, request, id):
        sections = Section.objects.filter(a_id=id)
        sections_info = []
        for s in sections:
            sections_info.append({"sectionID": s.s_id, "name": s.name})
        return Response({"sections": sections_info})


class SectionView(APIView):
    def post(self, request, id):
        name = request.GET.get('name')
        activity = Activity.objects.get(id=id)
        section = Section(a_id=id, s_id=activity.section_cnt, name=name)
        section.save()
        activity.section_cnt += 1
        activity.save()
        section.activity = activity
        section.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def delete(self, request, id, sectionID):
        Section.objects.filter(a_id=id, s_id=sectionID).delete()
        activity = Activity.objects.get(id=id)
        activity.section_cnt -= 1
        activity.save()
        response = {"status": 100, "msg": None}
        return Response(response)


class TranscriptFormView(APIView):
    def post(self, request, id, sectionID):
        transcript_format = str(request.data).replace('\'', '"')
        section = Section.objects.get(s_id=sectionID, a_id=id)
        section.transcript_format = transcript_format
        section.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def get(self, request, id, sectionID):
        transcript_format = Section.objects.get(s_id=sectionID, a_id=id).transcript_format;
        if transcript_format == '':
            return Response({'form': '{"question":[]}'})
        else:
            return Response({'form': transcript_format})


class AdmissionView(APIView):
    def post(self, request, id):
        wx_id = request.GET.get("wx_id")
        a = Application.objects.get(activity=id, candidate__wx_id=wx_id)
        a.admitted = False
        a.save()
        return Response({"status": 100})

    def get(self, request, id):
        wx_id = request.GET.get("wx_id")
        a = Application.objects.get(activity=id, candidate__wx_id=wx_id)
        a.admitted = True
        a.save()
        return Response({"status": 100})


class CandidateListForAdminView(APIView):
    def get(self, request):
        response = {"msg": None, "candidates": []}
        s_ID = request.GET.get("s_ID")
        # stage和s_ID的对应关系还需要进一步确定
        if s_ID == -1:
            candidate_list = Application.objects.filter(activity=cur_activity_id)
            for candidate in candidate_list:
                json_obj = {
                    "name": candidate.candidate.name,
                    "ID": candidate.candidate.student_id
                }
                response["candidates"].append(json_obj)
        else:
            candidate_list = Application.objects.filter(activity=cur_activity_id, stage=s_ID)
            for candidate in candidate_list:
                json_obj = {
                    "name": candidate.candidate.name,
                    "ID": candidate.candidate.student_id,
                    "wxID": candidate.candidate.wx_id
                }
                response["candidates"].append(json_obj)
        return Response(response)


class CandidateDetailForAdminView(APIView):
    def get(self, request):
        response = {"msg": None, "candidate": None}
        wxID = request.GET.get("wxID")
        candidate = Application.objects.get(activity=cur_activity_id, candidate__wx_id=wxID)
        response["candidate"] = {
            "application": candidate.application_form,
            "transcript": candidate.transcript
        }
        return Response(response)

# class GetActivityDetailView(APIView):
#     def get(self, request):
#         response = {"status": 100, "msg": None, "form": None, "sections": []}
#         activity_id = request.GET.get('id')
#         activity = Activity.objects.get(id=activity_id)
#         if activity is None:
#             res = Response()
#             res.status_code = 404
#             return res
#         response["form"] = activity.application_format
#         section_list = Section.objects.filter(a_id=activity_id)
#         if len(section_list) > 0:
#             for obj in section_list:
#                 json_obj = {
#                     "id": obj.s_id,
#                     "name": obj.name,
#                 }
#                 response["sections"].append(json_obj)
#         return Response(response)


# class GetSectionView(APIView):
#     def get(self, request):
#         # response = {"status": 100, "msg": None, "form": None, "sections": []}
#         activity_id = request.GET.get('activityID')
#         section_id = request.GET.get('sectionID')
#         section = Section.objects.get(a_id=activity_id, s_id=section_id)
#
#         if section is None:
#             res = Response()
#             res.status_code = 404
#             return res
#         else:
#             name = section.name
#             transcript_format = json.loads(section.transcript_format)
#             return Response({"name": name, "form": transcript_format})
#
#         # return Response(response)

# 考生相关接口


class RegisterView(APIView):
    def post(self, request):
        code = request.data["code"]

        print(code)
        appID = "wxc9568dc74b390136"
        appSecret = "1bdc626b0ea48761d84e4b1762c59641"
        url = "https://api.weixin.qq.com/sns/jscode2session"
        res = requests.get(url+"?appid="+appID+"&secret="+appSecret+"&js_code="+code+"&grant_type=authorization_code")
        ress = json.loads(res.text)
        openID = ress["openid"]
        session_key = ress["session_key"]
        trd_session = openID + "-" + session_key
        candidates = Candidate.objects.filter(wx_id=openID)
        if len(candidates) == 0:
            Candidate.objects.create(wx_id=openID)
        return Response({"session": trd_session})

    def get(self, request):
        if cur_activity_id == -1:
            return Response({"status": 400})
        a = Activity.objects.get(id=cur_activity_id)
        return Response({"form": a.application_format})


class ApplyView(APIView):
    def post(self, request):
        if cur_activity_id == -1:
            return Response({"status": 400})

        session = request.GET.get('session')
        wx_id = session.split("-")[0]
        candidate = Candidate.objects.get(wx_id=wx_id)
        application_form = str(request.data).replace('\'', '"')
        candidate.name = request.data["姓名"]
        candidate.student_id = request.data["学号"]

        activity = Activity.objects.get(id=cur_activity_id)
        try:
            application = candidate.applications.get(a_id=cur_activity_id)
        except:
            application = Application(a_id=cur_activity_id, candidate=candidate,
                                      application_form=application_form, activity=activity)

        else:
            application.application_form = application_form
        sections = []
        for sec in activity.sections:
            sections.append(sec.transcript_format)
        application.transcript = str({"sections": sections})
        application.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    # def get(self, request):
    #     if cur_activity_id == -1:
    #         return Response({"status": 400})
    #
    #     session = request.GET.get('session')
    #     wx_id = session.split("-")[0]
    #
    #     candidate = Candidate.objects.get(wx_id=wx_id)
    #     response = {"form": candidate.applications.get(a_id=cur_activity_id).application_form}
    #     return Response(response)


class StatusView(APIView):
    def get(self, request):
        if cur_activity_id == -1:
            return Response({"status": 400})

        session = request.GET.get('session')
        wx_id = session.split("-")[0]
        candidate = Candidate.objects.get(wx_id=wx_id)
        stage = candidate.applications.get(a_id=cur_activity_id).stage
        section = Section.objects.get(a_id=cur_activity_id, s_id=stage)
        response = {"status": "您的下一步是" + section.name + "请在113教室内等待"}
        return Response(response)


# 考官相关接口


class AuthExaminerLoginView(APIView):
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


class SectionExaminerView(APIView):
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


class CandidateListExaminerView(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "candidates": []}
        s_id = request.GET.get('s_ID')
        candidate_list = Application.objects.filter(stage=s_id)
        for candidate in candidate_list:
            jsonobj = {
                "name": candidate.candidate.name,
                "ID": candidate.candidate.ID,
                "wxID": candidate.candidate.wx_id
            }
            response["candidates"].append(jsonobj)
        return Response(response)


class TranscriptView(APIView):
    def get(self, request):
        if cur_activity_id == -1:
            return Response({"status": 400})

        response = {"status": 100, "msg": None, "application": None, "transcript": None}
        wxID = request.GET.get("wxID")
        candidate = Application.objects.get(candidate__wx_id=wxID, activity=cur_activity_id)
        response["application"] = candidate.application_form
        response["transcript"] = candidate.transcript
        return Response(response)

    def post(self, request):
        if cur_activity_id == -1:
            return Response({"status": 400})

        response = {"status": 100, "msg": None}
        wxID = request.GET.get("wxID")
        s_ID = request.GET.get("s_ID")
        candidate = Application.objects.get(candidate__wx_id=wxID, activity=cur_activity_id)
        transcrpit = json.loads(candidate.transcript)["sections"]
        for sec in transcrpit:
            if sec["sectionID"] == s_ID:
                sec["answer"] = str(request.data).replace('\'', '"')
                break
        candidate.transcript = json.dumps({"sections": transcrpit})
        candidate.save()
        return Response(response)
