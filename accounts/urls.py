from django.urls import path
from .views import UserRegister,UserRegisterViewSet,GetUserID
from rest_framework import routers


app_name = 'accounts'
urlpatterns = [
    path('register/',UserRegister.as_view(), name='register'),
    path('getid/',GetUserID.as_view(),name='get_id')
]

router = routers.SimpleRouter()
router.register('user', UserRegisterViewSet)
urlpatterns += router.urls