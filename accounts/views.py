from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer
from rest_framework import status


# Create your views here.
class UserRegister(APIView):
    def post(self, request):
        ser_user = UserRegisterSerializer(data=request.POST)
        if ser_user.is_valid():
            ser_user.create(ser_user.validated_data)
            return Response(ser_user.data, status=status.HTTP_201_CREATED)
        return Response(ser_user.errors, status=status.HTTP_400_BAD_REQUEST)
