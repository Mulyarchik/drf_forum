from rest_framework import generics
from . import serializers
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer