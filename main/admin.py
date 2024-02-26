from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Question)
admin.site.register(QuestionType)
admin.site.register(QuestionChoice)
admin.site.register(Survey)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyQuestionAnswer)
