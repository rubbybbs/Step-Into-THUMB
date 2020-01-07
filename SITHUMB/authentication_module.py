from rest_framework.authentication import BaseAuthentication
from SITHUMB import models
from SITHUMB import views
from rest_framework.exceptions import NotAuthenticated
from SITHUMB.token_module import get_token, out_token
from django.shortcuts import redirect

class TokenAuth2(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get("token")
        name = request.GET.get("uname")
        token_obj = out_token(name, token)
        if token_obj:
            return
        else:
            raise NotAuthenticated("You need login!")
