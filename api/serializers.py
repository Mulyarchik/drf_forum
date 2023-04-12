from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.fields import CurrentUserDefault

from .models import Tag, Question, Voting

User = get_user_model()


class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


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
