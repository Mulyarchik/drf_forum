from rest_framework import routers

from api import views
from api.views import LoginAPI, RegisterAPI, TagViewSet, AnswerViewSet, QuestionViewSet, CommentViewSet
from knox import views as knox_views
from django.urls import path

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet, basename='Tag')
router.register(r'questions', QuestionViewSet, basename='Question')
router.register(r'answers', AnswerViewSet, basename='Answer')
router.register(r'comments', CommentViewSet, basename='Comment')

urlpatterns = [
    path('accounts/register/', RegisterAPI.as_view(), name='register'),
    path('accounts/login/', LoginAPI.as_view(), name='login'),
    path('accounts/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('accounts/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    # path('questions/<int:pk>/vote/', views.AnswerLike.as_view()),  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # path('answers/<int:pk>/vote/', views.AnswerLike.as_view()),

]
urlpatterns += router.urls
