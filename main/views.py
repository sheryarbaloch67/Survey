from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .models import *
from .serializers import *
from django.db.models import Prefetch


@api_view(["GET", "POST"])
def create_survey(request):
    if request.method == "GET":
        question_types_all = QuestionType.objects.all()
        question_types = QuestionTypeSerializer(question_types_all, many=True).data
        return render(request, "create_survey.html", {"question_types": question_types})

    if request.method == "POST":
        survey_serializer = SurveySerializer(data=request.data)
        if not survey_serializer.is_valid():
            return Response(
                survey_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        indicator_count = sum(
            value == "start" for value in request.data.getlist("questions[indicator]")
        )

        print(indicator_count)

        if not 5 <= indicator_count <= 10:
            return Response(
                {"error": "Number of questions must be between 5 and 10"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_questions = []

        for i in range(1, indicator_count + 1):
            question_text = request.data.get(f"questions[{i}][text]")
            question_order = request.data.get(f"questions[{i}][order]")
            question_type_id = request.data.get(f"questions[{i}][type]")

            question_serializer = QuestionSerializer(
                data={
                    "text": question_text,
                    "type": question_type_id,
                    "order": question_order,
                }
            )
            if not question_serializer.is_valid():
                return Response(
                    question_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            question = question_serializer.save()
            created_questions.append(question)

            if request.data[f"questions[{i}][type]"] == "3":
                # choices_data = request.data.get(f"questions[{i}][choices]", [])
                for j in range(4):
                    choice_text = request.data[f"questions[{i}][choices][{j}][text]"]
                    choice_serializer = QuestionChoiceSerializer(
                        data={"question": question.id, "text": choice_text}
                    )
                    if choice_serializer.is_valid():
                        choice_serializer.save()
                    else:
                        return Response(
                            choice_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST,
                        )
        survey = survey_serializer.save()

        for question in created_questions:
            survey_question_serializer = SurveyQuestionSerializer(
                data={"survey": survey.id, "question": question.id}
            )
            if survey_question_serializer.is_valid():
                survey_question_serializer.save()
            else:
                return Response(
                    survey_question_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(survey_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def answer_survey(request, survey_id):
    if request.method == "GET":
        survey_questions = SurveyQuestion.objects.filter(survey_id=survey_id)

        for question in survey_questions:
            choices = QuestionChoice.objects.filter(question=question.question)
            question.choices = choices

        return render(
            request,
            "answer_survey.html",
            {"survey_questions": survey_questions, "survey_id": survey_id},
        )

    if request.method == "POST":
        survey_questions = SurveyQuestion.objects.filter(survey_id=survey_id)
        print(request.data)
        print(request.data.get("answers[87]"))

        question_ids = []

        for question in survey_questions:
            question_id = question.question.id
            question_ids.append(question_id)

            answer_data = request.data.get(f"answers[{question_id}]")

            if question.question.type.type == "Text":
                answer_type = "text_answer"
            elif question.question.type.type == "Number":
                answer_type = "number_answer"
            elif question.question.type.type == "Dropdown":
                answer_type = "choice_answer"

            print(f"Answer Data is {answer_data}")
            serializer = SurveyQuestionAnswerSerializer(
                data={"survey_question": question.id, f"{answer_type}": answer_data}
            )
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Answers saved successfully"}, status=status.HTTP_201_CREATED
        )


@api_view(["GET"])
def view_survey_answers(request, survey_id):
    try:
        survey = Survey.objects.get(id=survey_id)  # Check for survey existence
        survey_answers = SurveyQuestionAnswer.objects.filter(
            survey_question__survey_id=survey_id
        )

        serializer = SurveyQuestionAnswerSerializer(survey_answers, many=True)
        return Response(serializer.data)

    except (Survey.DoesNotExist, SurveyQuestionAnswer.DoesNotExist):
        return Response(
            {"message": "Survey answers not found"}, status=status.HTTP_404_NOT_FOUND
        )
