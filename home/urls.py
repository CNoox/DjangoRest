from django.urls import path
from .views import HomeView ,QuestionListView, CreateQuestionView, UpdateQuestionView, DeleteQuestionView, UserPhotoViewSet
from rest_framework import routers

app_name = 'home'
urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('quest/', QuestionListView.as_view()),
    path('quest/create/', CreateQuestionView.as_view()),
    path('quest/update/<int:pk>/', UpdateQuestionView.as_view()),
    path('quest/delete/<int:pk>/', DeleteQuestionView.as_view()),
]

router = routers.SimpleRouter()
router.register('photos', UserPhotoViewSet)
urlpatterns += router.urls