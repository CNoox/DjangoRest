from rest_framework import serializers
from .custom_relational_fields import UsernameEmailRelationalField
from .models import Question, Answer, UserPhoto


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user = UsernameEmailRelationalField(read_only=True)
    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        result = obj.answers.all()
        return AnswerSerializer(result, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Answer
        fields = '__all__'

class UserPhotoSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,slug_field='username')
    class Meta:
        model = UserPhoto
        fields = '__all__'