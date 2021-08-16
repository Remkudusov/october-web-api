from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField(editable=False)
    text = models.CharField(max_length=200)
    is_right = models.BooleanField()

    def __str__(self):
        return self.question.text + " " + self.text

    def save(self, *args, **kwargs):
        choices = Choice.objects.filter(question=self.question)

        if len(choices) == 0:
            self.number = 1
        else:
            self.number = choices[len(choices)-1].number + 1

        super().save(*args, **kwargs)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    points = models.IntegerField()

    def result(self):
        test_questions = Question.objects.filter(test=self.test)
        return str(int((self.points/len(test_questions)) * 100)) + "%"

    def __str__(self):
        return self.user.username + " " + self.test.name