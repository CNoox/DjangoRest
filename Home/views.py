from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person, Question
from .serializers import PersonSerializer, QuestionSerializer
from rest_framework import status


# Create your views here.

class HomeView(APIView):
    permission_classes = (IsAdminUser,)
    def get(self, request):
        persons = Person.objects.all()
        ser_person = PersonSerializer(instance=persons ,many=True).data
        return Response(data=ser_person)

class QuestionListView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        ser_question = QuestionSerializer(instance=questions ,many=True).data
        return Response(data=ser_question,status=status.HTTP_200_OK)

class CreateQuestionView(APIView):
    def post(self, request):
        ser_data = QuestionSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateQuestionView(APIView):
    def put(self, request, pk):
        question = Question.objects.get(pk=pk)
        ser_data = QuestionSerializer(instance=question, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteQuestionView(APIView):
    def delete(self, request, pk):
        question = Question.objects.get(pk=pk)
        question.delete()
        return Response({'message': 'deleted'},status=status.HTTP_204_NO_CONTENT)
