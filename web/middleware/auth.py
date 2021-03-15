from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """如果用户已登录，则request中赋值"""
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.user = user_object

        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.user:
            return redirect('web:login')