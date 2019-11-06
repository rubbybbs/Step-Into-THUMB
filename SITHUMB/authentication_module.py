from rest_framework.authentication import BaseAuthentication
from SITHUMB import models
from rest_framework.exceptions import NotAuthenticated
from SITHUMB.token_module import get_token, out_token


class TokenAuth2(BaseAuthentication):
    def authenticate(self, request):
        token = request.GET.get("token")
        name = request.GET.get("username")
        token_obj = out_token(name, token)
        if token_obj:
            return
        else:
            raise NotAuthenticated("你没有登入")
