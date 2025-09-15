from rest_framework import serializers

from Home.models import Question


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField(read_only=True)

class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        result = obj.answers.all()
        return AnswerSerializer(result, many=True).data


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'