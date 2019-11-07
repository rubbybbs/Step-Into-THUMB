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
    url(r'^Step-Into-THUMB/admin/login$', views.AuthAdminLogin.as_view()),
    url(r'^Step-Into-THUMB/admin/logintest$', views.LoginTest.as_view()),
    url(r'^Step-Into-THUMB/admin/home/create-activity$', views.CreateActivity.as_view()),
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-registration-form$', views.CreateRegisterForm.as_view()),
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-examiner$', views.CreateExaminer.as_view()),
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/create-section$', views.CreateSection.as_view()),
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/add-examiner$', views.AddExaminer.as_view()),
    url(r'^Step-Into-THUMB/admin/activity/(?P<id>[0-9]+)/section/(?P<sectionID>[0-9]+)/create-form$', views.CreateForm.as_view()),
]
