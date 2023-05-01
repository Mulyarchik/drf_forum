from django.db import transaction
from django.db.models import F
from psycopg2 import IntegrityError
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import mixins, status, generics, permissions, viewsets
from rest_condition import And, Or
from django.contrib.auth import login

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from .serializers import *
from . import serializers
from .models import Tag, Question, Voting, Answer, Comment, UserVoting, AlreadyVoted
from .permissions import IsReadOnlyRequest, IsDeleteRequest, IsPostRequest

User = get_user_model()


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class TagViewSet(generics.GenericAPIView, viewsets.ViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [Or(And(IsReadOnlyRequest),
                             And(IsPostRequest),
                             And(IsDeleteRequest))]

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return serializers.QuestionSerializer
        if self.request.method == 'PATCH':
            return serializers.QuestionUpdateSerializer

    def perform_create(self, serializer):
        voting = Voting.objects.create()
        serializer.save(voting=voting)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return serializers.AnswerSerializer
        if self.request.method == 'PATCH':
            return serializers.AnswerUpdateSerializer

    def perform_create(self, serializer):
        voting = Voting.objects.create()
        serializer.save(voting=voting)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return serializers.CommentSerializer
        if self.request.method == 'PATCH':
            return serializers.CommentUpdateSerializer


class QuestionVote(generics.CreateAPIView, generics.GenericAPIView):
    queryset = UserVoting.objects.all()
    serializer_class = UserVotingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = Question.objects.get(pk=self.kwargs['pk'])

        try:
            question.voting.set_vote(serializer.validated_data)
        except AlreadyVoted:
            return Response(status=status.HTTP_409_CONFLICT)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerVote(generics.CreateAPIView, generics.GenericAPIView):
    queryset = UserVoting.objects.all()
    serializer_class = UserVotingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = Answer.objects.get(pk=self.kwargs['pk'])

        try:
            answer.voting.set_vote(serializer.validated_data)
        except AlreadyVoted:
            return Response(status=status.HTTP_302_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
