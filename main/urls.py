from django.urls import path
from .views import *

urlpatterns = [
    path("create_survey/", create_survey, name="create_survey"),
    path("answer-survey/<int:survey_id>/", answer_survey, name="answer_survey"),
    path(
        "view_answers/<int:survey_id>/", view_survey_answers, name="view_survey_answers"
    ),
]
