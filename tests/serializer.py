from django.contrib.auth.models import User

from .models import *

from rest_framework import serializers
import re

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password'
        )

    def validate(self, data):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not (re.fullmatch(regex, data['email'])):
            raise serializers.ValidationError("Email is invalid!")
        
        if data['username'] == "" or data['email'] == "" or data['password'] == "":
            raise serializers.ValidationError("All fields must contain information")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = (
            'number', 'text'
        )

class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    def get_choices(self, obj):
        choices_objects = Choice.objects.filter(question=obj)
        return ChoiceSerializer(choices_objects, many=True).data

    class Meta:
        model = Question
        fields = (
            'text', 'choices'
        )

class TestSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        question_objects = Question.objects.filter(test=obj)
        return QuestionSerializer(question_objects, many=True).data

    class Meta:
        model = Test
        fields = (
            'id', 'name', 'description', 'questions'
        )

class PostAnswerSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    answers = serializers.ListField(
            child=serializers.IntegerField()
        )

    def validate(self, data):
        test = Test.objects.get(id=data['test_id'])
        questions = Question.objects.filter(test=test)
        if len(data['answers']) != len(questions):
            raise serializers.ValidationError("There must be answers on all questions of test!")
        return data

class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = (
            'user', 'test', 'points', 'result'
        )