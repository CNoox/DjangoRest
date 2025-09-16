from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from home.models import User
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from django.core.paginator import Paginator


# Create your views here.

class UserRegisterViewSet(viewsets.ViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self, request):
        """
        کاربران را مشاهده کنید
        """
        page_num = self.request.query_params.get('page',1)
        page_limit = self.request.query_params.get('limit',2)
        paginator = Paginator(self.queryset,page_limit)
        ser_user = UserSerializer(instance=paginator.page(page_num), many=True)
        return Response(ser_user.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        user_data = get_object_or_404(self.queryset, pk=pk)
        if user_data != request.user:
            return Response('You dont have access!')
        ser_user = UserSerializer(instance=user_data)
        return Response(data=ser_user.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        user_data = get_object_or_404(self.queryset, pk=pk)
        if user_data != request.user:
            return Response('You dont have access!')
        ser_user = UserSerializer(instance=user_data, data=request.data, partial=True)
        if ser_user.is_valid():
            ser_user.save()
            return Response(data=ser_user.data, status=status.HTTP_200_OK)
        return Response(ser_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user_data = get_object_or_404(self.queryset,pk=pk)
        if user_data != request.user:
            return Response('You dont have access!')
        user_data.is_active = False
        user_data.save()
        return Response({'message':'Account deactivated!'})

class UserRegister(APIView):
    """
    با استفاده از مقادیر زیر میتوانید حساب کاربری را بسازید
    """
    serializer_class = UserRegisterSerializer
    def post(self, request):
        ser_user = UserRegisterSerializer(data=request.data)
        if ser_user.is_valid():
            ser_user.create(ser_user.validated_data)
            return Response(ser_user.data, status=status.HTTP_201_CREATED)
        return Response(ser_user.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserID(APIView):
    """
    میتوانید از این بخش به آی دی حساب خود با استفاده از توکن دسترسی پیدا کنید
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle,]
    def get(self,request):
        return Response({'id':request.user.id})
