from django.test import TestCase, Client
from django.urls import reverse
from .models import Survey, Question, QuestionType, SurveyQuestion
from .serializers import *
from rest_framework import status
import json


class SurveyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_survey_url = reverse("create_survey")
        self.answer_survey_url = reverse("answer_survey", args=[1])
        self.view_survey_answers_url = reverse("view_survey_answers", args=[1])
        self.question_type_1 = QuestionType.objects.create(type="Text")
        self.question_type_2 = QuestionType.objects.create(type="Number")
        self.question_type_3 = QuestionType.objects.create(type="Dropdown")
        self.question = Question.objects.create(
            text="Sample Question", type=self.question_type_1, order=1
        )
        self.survey = Survey.objects.create(
            title="Sample Survey", description="Sample Description"
        )
        self.survey_question = SurveyQuestion.objects.create(
            survey=self.survey, question=self.question
        )

    def test_create_survey_valid_data(self):
        data = {
            "title": "Sample Survey",
            "description": "Sample Description",
            "questions[indicator]": ("start", "start", "start", "start", "start"),
            "questions[1][text]": "Sample Text Question",
            "questions[1][order]": 1,
            "questions[1][type]": self.question_type_1.id,
            "questions[2][text]": "Sample Number Question",
            "questions[2][order]": 2,
            "questions[2][type]": self.question_type_2.id,
            "questions[3][text]": "Sample Dropdown Question",
            "questions[3][order]": 3,
            "questions[3][type]": self.question_type_3.id,
            "questions[3][choices][0][text]": "Choice 1",
            "questions[3][choices][1][text]": "Choice 2",
            "questions[3][choices][2][text]": "Choice 3",
            "questions[3][choices][3][text]": "Choice 4",
            "questions[4][text]": "Sample Text Question 2",
            "questions[4][order]": 4,
            "questions[4][type]": self.question_type_1.id,
            "questions[5][text]": "Sample Number Question 2",
            "questions[5][order]": 5,
            "questions[5][type]": self.question_type_2.id,
        }
        response = self.client.post(self.create_survey_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_survey_missing_title(self):
        data = {
            "description": "Sample Description",
            "questions[indicator]": "start",
            "questions[1][text]": "Sample Question",
            "questions[1][order]": 1,
            "questions[1][type]": self.question_type_1.id,
        }
        response = self.client.post(self.create_survey_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_survey_valid_data(self):
        data = {
            "answers[1]": "Sample Answer",
        }
        response = self.client.post(self.answer_survey_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_answer_survey_missing_answer(self):
        data = {}
        response = self.client.post(self.answer_survey_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_survey_answers_valid_id(self):
        response = self.client.get(self.view_survey_answers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
