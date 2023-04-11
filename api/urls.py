from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.http.multipartparser import MultiPartParser
from api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users//', views.UserDetail.as_view()),
    path('tags/', views.UserList.as_view()),
    #path('tags//', views.UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
