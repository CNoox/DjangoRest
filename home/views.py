from rest_framework.permissions import IsAuthenticated, IsAdminUser ,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Question, UserPhoto
from .serializers import UserSerializer, QuestionSerializer, UserPhotoSerializer
from rest_framework import status,viewsets
from permissions import IsOwnerOrReadOnly
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import os


# Create your views here.

class HomeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        users = User.objects.all()
        page_num = self.request.query_params.get('page',1)
        page_limit = self.request.query_params.get('limit',2)
        paginator = Paginator(users,page_limit)
        ser_person = UserSerializer(instance=paginator.page(page_num) ,many=True).data
        return Response(data=ser_person)

class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        ser_question = QuestionSerializer(instance=questions ,many=True).data
        return Response(data=ser_question,status=status.HTTP_200_OK)

class CreateQuestionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        ser_data = QuestionSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateQuestionView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        ser_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteQuestionView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        self.check_object_permissions(request, question)
        question.delete()
        return Response({'message': 'deleted'},status=status.HTTP_204_NO_CONTENT)



class UserPhotoViewSet(viewsets.ViewSet):
    queryset = UserPhoto.objects.all()
    permission_classes = [IsAuthenticated]


    def partial_update(self, request, pk):
        photo_data = get_object_or_404(self.queryset, pk=pk)

        if photo_data.user != request.user:
            return Response({'detail': 'You dont have permission!'}, status=status.HTTP_403_FORBIDDEN)

        if 'photo' in request.FILES:
            old_photo = photo_data.photo
            if old_photo and old_photo.name != 'profiles/':
                if os.path.isfile(old_photo.path):
                    os.remove(old_photo.path)

        ser_photo = UserPhotoSerializer(
            instance=photo_data,
            data=request.data,
            partial=True
        )

        if ser_photo.is_valid():
            ser_photo.save()
            return Response(ser_photo.data, status=status.HTTP_200_OK)
        return Response(ser_photo.errors, status=status.HTTP_400_BAD_REQUEST)


