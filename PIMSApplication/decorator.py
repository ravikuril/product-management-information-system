from attr import exceptions
from django.http import JsonResponse
from flask import request
from pyboot.exception import GenericApiException, AccessDeniedException
from functools import wraps

from rest_framework import authentication, status

from PIMSApplication.models import User

X_AUTH_TOKEN='123456789-123456789-123456789'

def secure(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            print(**kw)
            print(request.META)
            token = request.META.get('X_AUTH_TOKEN')
            print(token)
            if not token or token != X_AUTH_TOKEN:
                raise AccessDeniedException("Required headers missing")
        except Exception as e:
            raise AccessDeniedException("Required headers missing")
        return f(*args, **kw)
    return wrapper

class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_AUTHORIZATION')
        print(username)
        if not username:
            return JsonResponse({'message': 'Unauthorized Access!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(username=username)
            if user is None:
                return JsonResponse({'message': 'Unauthorized Access !'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return
        except User.DoesNotExist:
            return JsonResponse({'message': 'authentication failed !'}, status=status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED)
