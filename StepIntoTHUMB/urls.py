"""StepIntoTHUMB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
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
    path('activity.html', views.activity),
    path('modify.html', views.application_form),
    path('segment.html', views.application_segment),
    path('accountManage.html', views.application_account),
    
    url(r'^Step-Into-THUMB/admin/login$', views.AuthAdminLogin.as_view()),
    url(r'^Step-Into-THUMB/admin/logintest$', views.LoginTest.as_view()),


    url(r'^Step-Into-THUMB/admin/activity-list$', views.ActivityList.as_view()),
    # 类型 GET
    url(r'^Step-Into-THUMB/admin/create-activity$', views.ActivityResponse.as_view()),
    # 类型 POST 正文 含有活动名称、开始日期、结束日期的json
    url(r'^Step-Into-THUMB/admin/delete-activity$', views.ActivityResponse.as_view()),
    # 类型 DELETE 参数 activityID


    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/save-registration-form$', views.RegistrationForm.as_view()),
    # 类型 POST 正文 报名表的json
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/get-registration-form$', views.RegistrationForm.as_view()),
    # 类型 GET 返回 报名表的json


    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/examiner-list$', views.ExaminerList.as_view()),
    # 类型 GET  返回值 {"examiners": [考官信息列表（每个考官的信息包括username、password、sections:[]）]}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-examiner$', views.Examiner.as_view()),
    # 类型 POST 参数 "username": , "password": 正文: {"sections" : [sectionID的list]}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/delete-examiner$', views.Examiner.as_view()),
    # 类型 DELETE 参数 "username":


    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section-list$', views.SectionList.as_view()),
    # 类型 GET 返回 环节列表 {"sections": ["sectionID":, "name":]}
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-section$', views.Section.as_view()),
    # 类型 POST 参数 name
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/delete-section$', views.Section.as_view()),
    # 类型 DELETE
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/get-transcript-form$', views.TranscriptForm.as_view()),
    # 类型 GET
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/save-transcript-form$', views.TranscriptForm.as_view()),
    # 类型 POST 正文...


    # url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/application$', views.GetActivityDetail.as_view()),

    # activityID 使用 cur_activity_ID
    url(r'^Step-Into-THUMB/examiner/login$', views.AuthExaminerLogin.as_view()),
    url(r'^Step-Into-THUMB/examiner/get-section$', views.SectionExaminer.as_view()),
    url(r'^Step-Into-THUMB/examiner/get-candidate-list$', views.CandidateListExaminer.as_view()),
    url(r'^Step-Into-THUMB/examiner/transcript$', views.Transcript.as_view()),

    url(r'^Step-Into-THUMB/candidate/register$', views.Register.as_view()),
    url(r'^Step-Into-THUMB/candidate/submit-application$', views.Apply.as_view()),
    # POST 正文：。。。
    url(r'^Step-Into-THUMB/candidate/get-status$', views.Status.as_view()),
    # GET

]
