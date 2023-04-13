from api import views
from api.views import RegisterAPI
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('tags/', views.TagList.as_view()),
    path('tags/<int:pk>/', views.TagDetail.as_view()),
    path('tags/<int:pk>/delete/', views.TagDelete.as_view()),

    path('questions/', views.QuestionList.as_view()),
    path('questions/<int:pk>/view/', views.QuestionView.as_view()),
    path('questions/<int:pk>/update', views.QuestionUpdate.as_view()),
    path('questions/<int:pk>/delete/', views.QuestionDelete.as_view()),

    path('answers/', views.AnswerList.as_view()),
    path('answers/<int:pk>/view/', views.AnswerView.as_view()),
    path('answers/<int:pk>/update', views.AnswerUpdate.as_view()),
    path('answers/<int:pk>/delete/', views.AnswerDelete.as_view()),

    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/view/', views.CommentView.as_view()),
    path('comments/<int:pk>/update', views.CommentUpdate.as_view()),
    path('comments/<int:pk>/delete/', views.CommentDelete.as_view()),
]
