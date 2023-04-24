from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import CurrentUserDefault

from .models import Tag, Question, Voting, Answer, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class Response201AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
    user_id = serializers.IntegerField(required=True)


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class QuestionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, default=timezone.now)
    updated_at = serializers.DateTimeField(read_only=True, default=timezone.now)
    author_id = serializers.HiddenField(default=CurrentUserDefault())
    author = serializers.CharField(source='author.username', read_only=True)
    voting = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super(QuestionSerializer, self).__init__(*args, **kwargs)
        self.fields['author_id'].default = user.id

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'author', 'author_id', 'created_at', 'updated_at', 'tag', 'voting']


class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'content', 'tag')


class AnswerSerializer(serializers.ModelSerializer):
    author_id = serializers.HiddenField(default=CurrentUserDefault())
    author = serializers.CharField(source='author.username', read_only=True)
    voting = serializers.CharField(read_only=True)
    is_useful = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super(AnswerSerializer, self).__init__(*args, **kwargs)
        self.fields['author_id'].default = user.id

    class Meta:
        model = Answer
        fields = ['id', 'question', 'content', 'author', 'author_id', 'created_at', 'is_useful', 'voting']


class AnswerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'content')


class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.HiddenField(default=CurrentUserDefault())
    author = serializers.CharField(source='author.username', read_only=True)

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        super(CommentSerializer, self).__init__(*args, **kwargs)
        self.fields['author_id'].default = user.id

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_id', 'answer', 'content', 'created_at']


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'content')
