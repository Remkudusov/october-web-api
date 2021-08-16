from django.contrib import admin
# from django.contrib.auth.models import User

from django import forms
from .models import *

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('login', 'email')
#
# admin.site.register(User, UserAdmin)

class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

admin.site.register(Test, TestAdmin)

class ChoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"

    # def clean_is_right(self):
    #     print(self.cleaned_data['question'])
    #     print(len(Choice.objects.all()))
    #     choices = Choice.objects.filter(question=self.cleaned_data['question'])
    #     print(len(choices))
    #     print("Проверка прошла!")
    #
    #     print(self.cleaned_data['is_right'])
    #     if self.cleaned_data['is_right']:
    #         print(len(choices))
    #         if len(choices) != 0:
    #             for choice in choices:
    #                 print(choice.is_right)
    #                 if choice.is_right:
    #                     raise forms.ValidationError("Правильный ответ на вопрос может быть только один!")
    #
    #     return self.cleaned_data['is_right']

class ChoiceInline(admin.TabularInline):
    model = Choice
    form = ChoiceAdminForm
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'result')

admin.site.register(Answer, AnswerAdmin)