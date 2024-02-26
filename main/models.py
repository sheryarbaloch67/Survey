from django.db import models
from django.core.exceptions import ValidationError


class QuestionType(models.Model):
    type = models.CharField(max_length=20)


class Question(models.Model):
    text = models.CharField(max_length=255)
    type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()


class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, through="SurveyQuestion")


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class SurveyQuestionAnswer(models.Model):
    survey_question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    text_answer = models.TextField(blank=True)
    number_answer = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    choice_answer = models.ForeignKey(
        QuestionChoice, on_delete=models.CASCADE, blank=True, null=True
    )
