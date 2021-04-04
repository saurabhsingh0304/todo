# from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from . models import UserProfile


class APIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        apikey = request.META.get('HTTP_APIKEY')
        if apikey is None:
            apikey = request.GET.get('api_key')
        if not apikey:
            return None
        try:
            userprofile = UserProfile.objects.get(key=apikey)
        except UserProfile.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return userprofile, None
