"""StepIntoTHUMB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', HomeView.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from SITHUMB import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index.html', views.index),
    path('activity.html', views.activity),
    path('modify.html', views.application_form),
    path('segment.html', views.application_segment),
    path('accountManage.html', views.application_account),
    path('finalcheck.html', views.application_finalcheck),
    path('score.html', views.application_score),
    path('CandidateDetail.html', views.application_detail),
    path('history.html', views.application_history),
    
    url(r'^Step-Into-THUMB/admin/login$', views.AuthAdminLoginView.as_view()),
    url(r'^Step-Into-THUMB/admin/logintest$', views.LoginTestView.as_view()),


    url(r'^Step-Into-THUMB/admin/activity-list$', views.ActivityListView.as_view()),
    # 类型 GET
    url(r'^Step-Into-THUMB/admin/create-activity$', views.ActivityView.as_view()),
    # 类型 POST 正文 含有活动名称、开始日期、结束日期的json
    url(r'^Step-Into-THUMB/admin/delete-activity$', views.ActivityView.as_view()),
    # 类型 DELETE 参数 activityID

    url(r'^Step-Into-THUMB/admin/start-activity$', views.ActivityStatusView.as_view()),
    # 锁定报名表 发布活动 开始报名  类型 GET 参数 activityID
    url(r'^Step-Into-THUMB/admin/stop-activity$', views.ActivityStatusView.as_view()),
    # 结束报名  类型 POST 参数 activityID

    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/save-registration-form$', views.RegistrationFormView.as_view()),
    # 类型 POST 正文 报名表的json
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/get-registration-form$', views.RegistrationFormView.as_view()),
    # 类型 GET 返回 报名表的json


    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/examiner-list$', views.ExaminerListView.as_view()),
    # 类型 GET  返回值 {"examiners": [考官信息列表（每个考官的信息包括username、password、sections:[]）]}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-examiner$', views.ExaminerView.as_view()),
    # 类型 POST 参数 "username": , "password": 正文: {"sections" : [sectionID的list]}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/delete-examiner$', views.ExaminerView.as_view()),
    # 类型 DELETE 参数 "username":

    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section-list$', views.SectionListView.as_view()),
    # 类型 GET 返回 环节列表 {"sections": ["sectionID":, "name":]}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-section$', views.SectionView.as_view()),
    # 类型 POST 参数 name
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/delete-section$', views.SectionView.as_view()),
    # 类型 DELETE
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/get-transcript-form$', views.TranscriptFormView.as_view()),
    # 类型 GET
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/save-transcript-form$', views.TranscriptFormView.as_view()),
    # 类型 POST 正文...


    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/get-candidate-list$', views.CandidateListForAdminView.as_view()),
    # 类型 GET  参数 s_ID
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/get-candidate-detail$', views.CandidateDetailForAdminView.as_view()),
    # 类型 GET  参数 wx_ID
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/add-comment$', views.CommentForCandidateView.as_view()),
    # 类型POST  参数 wx_ID 正文 评论内容
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/admission/admit$', views.AdmissionView.as_view()),
    # 类型 GET  参数 wx_ID
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/admission/refuse$', views.AdmissionView.as_view()),
    # 类型 POST 参数 wx_ID
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/send_message$', views.SendMessageView.as_view()),
    # 类型 POST {"admission":..., "refusal":...}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/get-excel-data$', views.ExportExcelView.as_view()),

    # url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/application$', views.GetActivityDetailView.as_view()),

    # activityID 使用 cur_activity_ID
    url(r'^Step-Into-THUMB/examiner/login$', views.AuthExaminerLoginView.as_view()),
    url(r'^Step-Into-THUMB/examiner/get-section$', views.SectionExaminerView.as_view()),
    url(r'^Step-Into-THUMB/examiner/get-candidate-list$', views.CandidateListExaminerView.as_view()),
    url(r'^Step-Into-THUMB/examiner/get-history-candidate-list$', views.HistoryCandidateListExaminerView.as_view()),
    url(r'^Step-Into-THUMB/examiner/transcript$', views.TranscriptView.as_view()),

    # get  {"sections":[{"sectionID":.., "question":[{"name":,"type":,"answer":},...]}]}
    # post 参数：s_id:, eligible：0(不通过)/1(通过), username  正文：{}



    url(r'^Step-Into-THUMB/candidate/register$', views.RegisterView.as_view()),
    # POST 参数：code  返回 {"3rdsession":  }
    url(r'^Step-Into-THUMB/candidate/get-empty-form$', views.RegisterView.as_view()),
    # GET
    url(r'^Step-Into-THUMB/candidate/submit-application$', views.ApplyView.as_view()),
    # POST 参数:session  正文：报名表json 每个问题项相较空表加一个"answer"的字段
    url(r'^Step-Into-THUMB/candidate/get-status$', views.StatusView.as_view()),
    # GET 参数：session


]
