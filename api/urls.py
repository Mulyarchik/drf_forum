from django.urls import path
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('tags/<int:pk>/', views.TagDetail.as_view()),
    path('questions/', views.QuestionList.as_view()),
    path('questions/<pk>/', views.QuestionDetail.as_view()),
]
