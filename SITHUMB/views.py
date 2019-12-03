from django.shortcuts import render

# Create your views here.

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import *
from SITHUMB.token_module import get_token
from SITHUMB.authentication_module import TokenAuth2
import requests
import json
from django.views.decorators.csrf import csrf_exempt

cur_activity_id = -1

def update_cur_activity():
    global cur_activity_id
    try:
        cur_activity_id = Activity.objects.get(status=1).id
    except Exception:
        pass


update_cur_activity()


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
    return render(request, "CandidateDetail.html")


def application_score(request):
    return render(request, "score.html")


def application_history(request):
    return render(request, "history.html")


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
        activity.application_format = "{\"id\":" + str(activity.id) + ", \"question\": [{\"name\": \"姓名\", \"type\": " \
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
        update_cur_activity()
        response = {"status": 100, "a_id": activity_id}
        return Response(response)

    def post(self, request):
        activity_id = request.GET.get("activityID")
        a = Activity.objects.get(id=activity_id)
        a.status = 2
        a.save()
        update_cur_activity()
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
            return Response({'status': activity.status, 'form': '{"question":[]}'})
        else:
            return Response({'status': activity.status, 'form': activity.application_format})


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
                                       "password": e.password,
                                       "sections": sections_info})
            return Response({'status': activity.status, "count": examiners_count, "data": examiners_info})


class ExaminerView(APIView):
    def post(self, request, id):
        username = request.GET.get('username')
        password = request.GET.get('password')
        sections = request.data["sections"]

        examiner = User(username=username, password=make_password(password))
        examiner.save()
        examiner.extension.activity = Activity.objects.get(id=id)
        # 创建历史考生列表结构
        examinees = {
            "sections": []
        }
        for s_id in sections:
            examiner.extension.sections.add(Section.objects.get(s_id=s_id, activity__id=id))
            json_obj = {
                "s_ID": s_id,
                "candidates": []
            }
            examinees["sections"].append(json_obj)
        examiner.extension.examinees = json.dumps(examinees)
        examiner.extension.password = password
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
        sections = Section.objects.filter(activity__id=id).order_by("s_id")
        sections_info = []
        for s in sections:
            sections_info.append({"sectionID": s.s_id, "compulsory": s.compulsory, "name": s.name})
        return Response({'status': activity.status, "sections": sections_info})


class SectionView(APIView):
    def post(self, request, id):
        name = request.GET.get('name')
        compulsory = request.GET.get("compulsory")
        activity = Activity.objects.get(id=id)
        section = Section(s_id=activity.section_cnt, name=name, compulsory=compulsory, activity=activity)
        section.save()
        activity.section_cnt += 1
        activity.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def delete(self, request, id, sectionID):
        Section.objects.filter(activity__id=id, s_id=sectionID).delete()
        activity = Activity.objects.get(id=id)
        activity.section_cnt -= 1
        activity.save()
        response = {"status": 100, "msg": None}
        return Response(response)


class TranscriptFormView(APIView):
    def post(self, request, id, sectionID):
        transcript_format = str(request.data).replace('\'', '"')
        section = Section.objects.get(s_id=sectionID, activity__id=id)
        section.transcript_format = transcript_format
        section.save()
        response = {"status": 100, "msg": None}
        return Response(response)

    def get(self, request, id, sectionID):
        transcript_format = Section.objects.get(s_id=sectionID, activity__id=id).transcript_format;
        if transcript_format == '':
            return Response({'form': '{"question":[]}'})
        else:
            return Response({'form': transcript_format})


class AdmissionView(APIView):
    def post(self, request, id):
        wx_id = request.GET.get("wx_id")
        a = Application.objects.get(activity__id=id, candidate__wx_id=wx_id)
        a.admitted = False
        a.save()
        return Response({"status": 100})

    def get(self, request, id):
        wx_id = request.GET.get("wx_id")
        a = Application.objects.get(activity__id=id, candidate__wx_id=wx_id)
        a.admitted = True
        a.save()
        return Response({"status": 100})


class CandidateListForAdminView(APIView):
    def get(self, request, id):
        response = {"code": 0, "msg": None, "count": 0, "data": []}
        s_ID = int(request.GET.get("s_ID"))
        # stage和s_ID的对应关系还需要进一步确定
        # s_ID与显示的考生列表关系如下：
        # 1） 当section为必须通过时，其前置必须通过的section也必须全部通过，才显示
        # 2） 当section为非必须通过时，只要考过试，就显示。
        if s_ID == -1:
            res_list = Application.objects.filter(activity__id=id)
        elif s_ID == -2:
            sections = Section.objects.filter(activity__id=id, compulsory=True).order_by("s_id")
            res_list = sections[0].unqualified.all()
        elif s_ID == -3:
            res_list = Application.objects.filter(admitted=True)
        else:
            section = Section.objects.get(activity__id=id, s_id=s_ID)
            res_list = section.qualified.all()

        for application in res_list:
            response["data"].append({
                "name": application.candidate.name,
                "ID": application.candidate.student_id,
                "wxID": application.candidate.wx_id,
                "admitted": application.admitted
            })
        response["count"] = len(res_list)
        return Response(response)


class CandidateDetailForAdminView(APIView):
    def get(self, request, id):
        response = {"msg": None,  "application": None, "transcript": None}
        wxID = request.GET.get("wxID")
        candidate = Application.objects.get(activity__id=id, candidate__wx_id=wxID)
        response["application"] = candidate.application_form
        response["transcript"] = candidate.transcript

        return Response(response)


class CommentForCandidateView(APIView):
    def post(self, request, id):
        response = {"msg": None}
        wxID = request.GET.get("wxID")
        candidiate = Application.objects.get(activity=id, candidate__wx_id=wxID)
        print(request.data)
        print(type(request.data))
        print(request.data["comment"])
        tmp = json.loads(candidiate.transcript)
        tmp["comment"]  = request.data["comment"]
        candidiate.transcript = json.dumps(tmp, ensure_ascii=False)
        candidiate.save()
        return Response(response)

# 考生相关接口
class RegisterView(APIView):
    def post(self, request):
        code = request.data["code"]

        print(code)
        appID = "wxc9568dc74b390136"
        appSecret = "1bdc626b0ea48761d84e4b1762c59641"
        url = "https://api.weixin.qq.com/sns/jscode2session"
        res = requests.get(
            url + "?appid=" + appID + "&secret=" + appSecret + "&js_code=" + code + "&grant_type=authorization_code")
        ress = json.loads(res.text)
        openID = ress["openid"]
        session_key = ress["session_key"]
        trd_session = openID + "-" + session_key
        candidates = Candidate.objects.filter(wx_id=openID)
        if len(candidates) == 0:
            # 创建考生对象
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
        activity = Activity.objects.get(id=cur_activity_id)
        candidate = Candidate.objects.get(wx_id=wx_id)
        application_form = str(request.data).replace('\'', '"')
        for q in request.data["question"]:
            if q["name"] == "姓名":
                candidate.name = q["answer"]
            elif q["name"] == "学号":
                candidate.student_id = q["answer"]
        candidate.save()

        try:
            application = candidate.applications.get(activity__id=cur_activity_id)
        except:
            # 创建评分表
            sections = Section.objects.filter(activity__id=cur_activity_id)
            transcript_obj = {
                "sections": [],
                "comment": ""
            }
            for sec in sections:
                if sec.transcript_format != "":
                    json_obj = {
                        "sectionID": sec.s_id,
                        "compulsory": str(sec.compulsory),
                        "passed": "undecided",
                        "name": sec.name,
                        "question": json.loads(sec.transcript_format)["question"],
                        "examiner": "null"
                    }
                    transcript_obj["sections"].append(json_obj)
                else:
                    # 实际上线时不会出现。
                    json_obj = {
                        "sectionID": sec.s_id,
                        "name": sec.name,
                        "question": [],
                        "examiner": "null"
                    }
                    transcript_obj["sections"].append(json_obj)

            application = Application(candidate=candidate, application_form=application_form,
                                      activity=activity, transcript=json.dumps(transcript_obj, ensure_ascii=False))
            application.save()
            sections = Section.objects.filter(activity__id=cur_activity_id)
            for sec in sections:
                sec.checking.add(application)
        else:
            application.application_form = application_form
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
        stage = candidate.applications.get(activity__id=cur_activity_id).stage
        section = Section.objects.get(activity__id=cur_activity_id, s_id=stage)
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
        if cur_activity_id == -1:
            return Response({"status": 404, "code": 404})
        response = {"code": 0, "msg": None, "count": 0, "data": []}
        s_id = request.GET.get('s_ID')
        checking_list = Section.objects.get(activity__id=cur_activity_id, s_id=s_id).checking.all()
        for e in checking_list:
            response["data"].append({
                "name": e.candidate.name,
                "ID": e.candidate.student_id,
                "wxID": e.candidate.wx_id
            })
        response["count"] = len(response["data"])
        return Response(response)


class HistoryCandidateListExaminerView(APIView):
    def get(self, request):
        response = {"code": 0, "msg": None, "count": 0, "data": []}
        username = request.GET.get('username')
        s_id = int(request.GET.get('s_ID'))
        examiner = Examiner.objects.get(username=username)
        sections = json.loads(examiner.examinees)["sections"]
        # 后评分的先显示
        for sec in sections:
            if s_id == int(sec["s_ID"]):
                response["count"] = len(sec["candidates"])
                for i in range(len(sec["candidates"])):
                    response["data"].append(sec["candidates"].pop())
        return Response(response)


class TranscriptView(APIView):
    def get(self, request):
        response = {"status": 100, "msg": None, "application": None, "transcript": None}
        wxID = request.GET.get("wxID")
        username = request.GET.get("username")
        examiner = Examiner.objects.get(username=username)
        candidate = Application.objects.get(candidate__wx_id=wxID, activity__id=examiner.activity.id)
        response["application"] = candidate.application_form
        response["transcript"] = candidate.transcript
        return Response(response)

    def post(self, request):
        if cur_activity_id == -1:
            return Response({"status": 400})

        response = {"status": 100, "msg": None}
        wx_id = request.GET.get("wxID")
        s_id = int(request.GET.get("s_ID"))
        eligible = int(request.GET.get("eligible"))
        sections = Section.objects.filter(activity__id=cur_activity_id).order_by("s_id")
        section = Section.objects.get(activity__id=cur_activity_id, s_id=s_id)
        username = request.GET.get("username")
        application = Application.objects.get(candidate__wx_id=wx_id, activity__id=cur_activity_id)
        transcript = json.loads(application.transcript)["sections"]
        examiner = Examiner.objects.get(username=username)
        histroy_candidate_list = json.loads(examiner.examinees)["sections"]
        for sec in transcript:
            if sec["sectionID"] == s_id:
                sec["question"] = request.data
                sec["examiner"] = username
                if sec["compulsory"] == "True":
                    # 考生是否通过
                    if eligible == 1:
                        sec["passed"] = "True"
                    elif eligible == 0:
                        sec["passed"] = "False"
                else:
                    sec["passed"] = "Pass"
                # 在考官的历史列表中加入该考生
                for s in histroy_candidate_list:
                    if int(s["s_ID"]) == s_id:
                        # 第一次评分的时候才加入历史记录
                        json_obj = {
                            "name": application.candidate.name,
                            "ID": application.candidate.student_id,
                            "wxID": application.candidate.wx_id
                        }
                        if json_obj not in s["candidates"]:
                            s["candidates"].append(json_obj)
                break
        application.transcript = '{"sections": ' + str(transcript).replace('\'', '\"') + '}'
        application.save()
        # 维护各个环节的通过/不通过字段
        # 若环节为必考且考生通过，通过字段中加入该考生，并将该考生移除出前一个必考环节的通过字段；
        # 若环节为必考且考生不通过，不通过字段中加入该考生
        # 若环节为非必考，在通过字段中直接加入
        compulsory_list = Section.objects.filter(activity__id=cur_activity_id, compulsory=True).order_by("s_id")
        compulsory_id_list = [sec.s_id for sec in compulsory_list]
        if section.compulsory:
            pos = compulsory_id_list.index(section.s_id)
            if eligible:
                section.qualified.add(application)
                if pos != 0:
                    compulsory_list[pos-1].qualified.remove(application)
            else:
                section.unqualified.add(application)
                for i in range(pos + 1, len(compulsory_list)):
                    compulsory_list[i].checking.remove(application)
        else:
            section.qualified.add(application)
        section.checking.remove(application)
        section.save()
        examiner.examinees = json.dumps({"sections": histroy_candidate_list}, ensure_ascii=False)
        examiner.save()
        return Response(response)
