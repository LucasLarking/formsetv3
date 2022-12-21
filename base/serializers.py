from rest_framework import serializers
from django.forms.models import model_to_dict
from .models import (
    Survey,
    Question,
    Option,
    Answer
)


# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = '__all__'


# class SurveySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Survey
#         fields = '__all__'

# MOSH
class SurveySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    survey = serializers.CharField(max_length=200)
    updated = serializers.DateTimeField()
    created = serializers.DateTimeField()
    quequestionNum = serializers.SerializerMethodField(
        method_name="questionNum")

    def questionNum(self, survey: Survey):
        return survey.question_set.all().count()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'survey', 'type']

    survey = serializers.HyperlinkedRelatedField(
        queryset=Survey.objects.all(),
        view_name='survey-detail'
    )

    # def validate(self, data):
    #     if data['']

    def create(self, validated_data):
        question = Question(**validated_data)
        question.other = 1
        question.save()
        return question

    def update(self, instance, validated_data):
        instance.question = validated_data.get('question')
        instance.save()
        return instance




# class QuestionSerializer(serializers.Serializer):
#     question = serializers.CharField(max_length=200)
#     survey = serializers.HyperlinkedRelatedField(
#         queryset=Survey.objects.all(),
#         view_name='survey-detail'
#     )

    # surveyy = SurveySerializer()
    # survey = serializers.StringRelatedField()
    # survey = serializers.PrimaryKeyRelatedField(
    #     queryset=Survey.objects.all()
    # )
