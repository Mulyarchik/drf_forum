from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.encoding import smart_str
from rest_framework import generics, response, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .models import Tag, Question, Voting
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import QuestionSerializer

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class TagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        new_voting = Voting.objects.create(count_down=0, count_up=0)
        serializer.save(voting=new_voting)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
