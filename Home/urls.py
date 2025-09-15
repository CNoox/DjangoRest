from django.urls import path
from .views import HomeView ,QuestionListView, CreateQuestionView, UpdateQuestionView, DeleteQuestionView
from rest_framework.authtoken import views as auth_views

app_name = 'home'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('quest/', QuestionListView.as_view()),
    path('quest/create/', CreateQuestionView.as_view()),
    path('quest/update/<int:pk>/', UpdateQuestionView.as_view()),
    path('quest/delete/<int:pk>/', DeleteQuestionView.as_view()),
]