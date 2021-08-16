from django.shortcuts import render
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout

from .models import *
from .serializer import *

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

def index(request):
    return render(request, "tests/index.html")

class sign_up_view(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class log_in_view(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        if username == "" or password == "":
            data = {
                "All fields must contain information!"
            }
            return Response(data)

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request=request, user=user)

            data = {
                "User is logged in!"
            }
            return Response(data)
        else:
            data = {
                'message': 'Account does not exist!',
                'username': username,
                'password': password
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

class log_out_view(APIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        data = {
            'message': "User logged out successfully!"
        }
        return Response(data)

class tests_view(APIView):
    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

class answer_view(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            serializer = PostAnswerSerializer(data=request.data)

            if serializer.is_valid():
                test = Test.objects.get(id=serializer.data['test_id'])
                all_questions = Question.objects.filter(test=test)
                points = 0

                for choice_index in range(len(serializer.data['answers'])):
                    choice = Choice.objects.filter(question=all_questions[choice_index],
                                                   number=serializer.data['answers'][choice_index])
                    if choice[0].is_right:
                        points += 1

                answer = Answer(user=request.user, test=test, points=points)
                answer.save()

                result = TestAnswerSerializer(answer)

                return Response(result.data)
            else:
                return Response(serializer.errors)
        else:
            data = {
                'message': "You are not authenticated in system. Do it with the log_in request."
            }
            return Response(data)