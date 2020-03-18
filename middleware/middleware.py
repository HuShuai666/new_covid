import json

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

import logging

from covid_19.settings import ignore_auth_urls

from utils.common.token import token_auth

logger = logging.getLogger("django")


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        url_path = request.path
        if url_path in ignore_auth_urls:
            return
        temp_url_list = ['/api/v1/user_info/reset_password/']
        start = str(url_path).find('/api/v1/user_info/')
        if start != -1 and url_path not in temp_url_list and request.method == 'GET':
            return
        logger.info('Auth Url ---------------------------> %s' % (request.method + ':  ' + url_path))
        token = request.META.get('HTTP_AUTHORIZATION') or request.META.get('HTTP_TOKEN')
        if not token:
            return HttpResponse(content=json.dumps(dict(code=400, msg='please take your token in header')),
                                content_type='application/json')
        try:
            user_id, is_student, is_refresh = token_auth(token)
        except Exception as e:
            logger.info('*' * 60)
            logger.info(e.__repr__())
            logger.info('*' * 60)
            return HttpResponse(content=json.dumps(dict(code=401, msg='token auth failed')))
        request.refresh_token = is_refresh
        if is_student == 1:
            user = StudentInfo.objects.filter(id=user_id).first()
        else:
            user = UserInfo.objects.filter(id=user_id).first()
        request.user = user
        request.is_student = is_student
        return

