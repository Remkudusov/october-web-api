from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('sign_up/', sign_up_view.as_view()),
    path('log_in/', log_in_view.as_view()),
    path('log_out/', log_out_view.as_view()),
    path('tests/', tests_view.as_view()),
    path('answer/', answer_view.as_view()),
]
