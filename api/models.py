from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from rest_framework import status
from rest_framework.response import Response


class AlreadyVoted(Exception):
    "Raised then users tries to vote on a question more than 1 time"
    pass


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='tag')

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.name)

    class Meta:
        app_label = 'api'


class Voting(models.Model):
    summary_rating = models.IntegerField(default=0, verbose_name='Summary rating')

    def __str__(self):
        return f"voting_id:{self.pk}, summary_rationg:{self.summary_rating}"

    def is_already_voted(self, user_id):
        try:
            if UserVoting.objects.get(voting_id=self.id, user_id=user_id):
                return True
        except ObjectDoesNotExist:
            return None

    @transaction.atomic
    def set_vote(self, data):
        user = data['user']
        value = data['value']

        if self.is_already_voted(user.id):
            raise AlreadyVoted
        # additional validation
        if value == -1:
            self.summary_rating -= 1
        elif value == 1:
            self.summary_rating += 1

        UserVoting.objects.create(value=value, voting_id=self.id, user_id=user.id)
        self.save()


class User(AbstractUser):
    voting = models.ManyToManyField(Voting, through='UserVoting')


class UserVoting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    value = models.IntegerField(choices={(1, 'vote up'), (-1, 'vote down')})

    # value = models.IntegerChoices('1', '-1')

    class Meta:
        unique_together = ['user', 'voting']


class Question(models.Model):
    title = models.CharField(max_length=500, verbose_name='Article title')
    content = models.CharField(max_length=1000, verbose_name='Content')
    author = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modified ')
    tag = models.ManyToManyField(Tag, blank=True)
    voting = models.OneToOneField('Voting', on_delete=models.CASCADE, blank=True, null=True)


class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True, verbose_name='question')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    content = models.CharField(max_length=1000, verbose_name='Comment')
    is_useful = models.BooleanField(verbose_name='Is Useful', null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
    voting = models.OneToOneField('Voting', on_delete=models.CASCADE, blank=True, null=True)


class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.PROTECT, blank=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    content = models.CharField(max_length=1000, verbose_name='Comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Asked')
