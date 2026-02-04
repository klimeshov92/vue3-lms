from django.shortcuts import render

# Create your views here.

from .models import *
from .filters import *
from .serializers import *
from bpms.serializers import *
from rest_framework import viewsets
from guardian.shortcuts import get_objects_for_user
from core.permissions import ObjectPermission
from guardian.utils import get_anonymous_user
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.pagination import CustomPageNumberPagination
from django.conf import settings
from guardian.shortcuts import get_objects_for_user
from guardian.utils import get_anonymous_user
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
import json
import random
from django.http import JsonResponse
from django.db.models import Sum
from django.db.models import Q

import logging
logger = logging.getLogger('project')

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = SurveyFilter
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return SurveyEditSerializer
        elif self.action == 'partial_update':
            return SurveyEditSerializer
        return SurveySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class SurveySectionViewSet(viewsets.ModelViewSet):
    queryset = SurveySection.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['name']
    ordering = ['name']

    permission_map = {
        'create': 'surveys.add_survey',
        'retrieve': 'surveys.view_survey',
        'update': 'surveys.change_survey',
        'partial_update': 'surveys.change_survey',
        'destroy': 'surveys.delete_survey',
        'list': 'surveys.view_survey',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_survey =self._object.survey
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            survey = None
            if self.action == 'create':
                survey_id = self.request.data.get('survey')
                if survey_id:
                    survey = Survey.objects.filter(pk=survey_id).first()
            elif self.action == 'list':
                survey_id = self.request.query_params.get('survey')
                if survey_id:
                    survey = Survey.objects.filter(pk=survey_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                survey = getattr(self, '_related_survey', None)

            if survey and not self.request.user.has_perm(perm_codename, survey):
                self.permission_denied(self.request, message='Недостаточно прав на тест')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для теста {survey}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return SurveySectionEditSerializer
        elif self.action == 'partial_update':
            return SurveySectionEditSerializer
        return SurveySectionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class SurveySectionQuestionViewSet(viewsets.ModelViewSet):
    queryset = SurveySectionQuestion.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['item']
    ordering = ['item']

    permission_map = {
        'create': 'surveys.add_survey',
        'retrieve': 'surveys.view_survey',
        'update': 'surveys.change_survey',
        'partial_update': 'surveys.change_survey',
        'destroy': 'surveys.delete_survey',
        'list': 'surveys.view_survey',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_survey = self._object.survey_section.survey
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            survey = None
            if self.action == 'create':
                survey_section_id = self.request.data.get('survey_section')
                if survey_section_id:
                    survey = SurveySection.objects.select_related('survey').get(pk=survey_section_id).survey
            elif self.action == 'list':
                survey_section_id = self.request.query_params.get('survey_section')
                if survey_section_id:
                    survey = SurveySection.objects.select_related('survey').get(pk=survey_section_id).survey
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                survey = getattr(self, '_related_survey', None)

            if survey and not self.request.user.has_perm(perm_codename, survey):
                self.permission_denied(self.request, message='Недостаточно прав на тест')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для теста {survey}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return SurveySectionQuestionEditSerializer
        elif self.action == 'partial_update':
            return SurveySectionQuestionEditSerializer
        return SurveySectionQuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [AllowAny, ObjectPermission]
    pagination_class = CustomPageNumberPagination
    filterset_class = QuestionFilter
    ordering_fields = ['text']
    ordering = ['text']

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionEditSerializer
        elif self.action == 'partial_update':
            return QuestionEditSerializer
        return QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    def get_object(self):
        obj = super().get_object()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['item']
    ordering = ['item']

    permission_map = {
        'create': 'surveys.add_question',
        'retrieve': 'surveys.view_question',
        'update': 'surveys.change_question',
        'partial_update': 'surveys.change_question',
        'destroy': 'surveys.delete_question',
        'list': 'surveys.view_question',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_question =self._object.question
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            question = None
            if self.action == 'create':
                question_id = self.request.data.get('question')
                if question_id:
                    question = Question.objects.filter(pk=question_id).first()
            elif self.action == 'list':
                question_id = self.request.query_params.get('question')
                if question_id:
                    question = Question.objects.filter(pk=question_id).first()
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                question = getattr(self, '_related_question', None)

            if question and not self.request.user.has_perm(perm_codename, question):
                self.permission_denied(self.request, message='Недостаточно прав на вопрос')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для вопроса {question}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return AnswerEditSerializer
        elif self.action == 'partial_update':
            return AnswerEditSerializer
        return AnswerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

class RelevantPointViewSet(viewsets.ModelViewSet):
    queryset = RelevantPoint.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['text']
    ordering = ['text']

    permission_map = {
        'create': 'surveys.add_question',
        'retrieve': 'surveys.view_question',
        'update': 'surveys.change_question',
        'partial_update': 'surveys.change_question',
        'destroy': 'surveys.delete_question',
        'list': 'surveys.view_question',
    }

    def get_object(self):
        if hasattr(self, '_object'):
            return self._object
        self._object = super().get_object()
        self._related_question = self._object.answer.question
        logger.debug(
            f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {self._object.pk}"
        )
        return self._object

    def get_permissions(self):
        perm_codename = self.permission_map.get(self.action)
        if perm_codename:
            question = None
            if self.action == 'create':
                answer_id = self.request.data.get('answer')
                if answer_id:
                    question = Answer.objects.select_related('question').get(pk=answer_id).question
            elif self.action == 'list':
                answer_id = self.request.query_params.get('answer')
                if answer_id:
                    question = Answer.objects.select_related('question').get(pk=answer_id).question
            elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                question = getattr(self, '_related_question', None)

            if question and not self.request.user.has_perm(perm_codename, question):
                self.permission_denied(self.request, message='Недостаточно прав на вопрос')
            else:
                logger.debug(
                    f"Пользователь '{self.request.user}' имеет права '{perm_codename}' для вопроса {question}"
                )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return RelevantPointEditSerializer
        elif self.action == 'partial_update':
            return RelevantPointEditSerializer
        return RelevantPointSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Параметры запроса: {self.request.query_params}")
        return queryset

    #def get_object(self):
        #obj = super().get_object()
        #logger.debug(f"Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Объект ID: {obj.pk}")
        #return obj

    def perform_create(self, serializer):
        logger.debug(f"Создаем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_update(self, serializer):
        logger.debug(f"Обновляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}, Данные: {self.request.data}")
        object = serializer.save()

    def perform_destroy(self, instance):
        logger.debug(f"Удаляем через ViewSet, Метод HTTP: {self.request.method}, Заголовки: {self.request.headers}")
        instance.delete()

@api_view(['GET'])
@permission_classes([AllowAny])
def survey_attempt(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        survey = task.survey
        result = task.survey_result

        executor = result.task.executor == request.user

        if not executor:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        attempt_available = survey.attempts > result.attempts
        logger.debug(f"Использовано попыток: {result.attempts} из {survey.attempts}. Есть еще попытки: {attempt_available}")

        last_attempt = result.survey_attempts.lasurvey('id') if result.survey_attempts.exists() else None
        logger.debug(f"Последняя попытка прохождения теста: {last_attempt}")

        last_attempt_end = last_attempt.end_time if last_attempt else None
        logger.debug(f"Последняя попытка прохождения теста завершена: {last_attempt_end}")

        need_create_attempt = (
            (last_attempt and last_attempt_end and attempt_available) or
            (not last_attempt and attempt_available)
        )
        logger.debug(f"Необходимо создать попытку: {need_create_attempt}")

        if need_create_attempt:
            logger.debug(f"Создание попытки для результата теста: {result}")

            if not survey.survey_sections.exists():
                return Response({"error": "Нет разделов в тесте"}, status=403)
            if not SurveySectionQuestion.objects.filter(survey_section__in=survey.survey_sections.all()).exists():
                return Response({"error": "В разделах нет вопросов"}, status=403)

            survey_attempt = SurveyAttempt.objects.create(
                survey_result=result,
                number = result.survey_attempts.count() + 1,
                status='assigned',
                start_time=timezone.now(),
                plan_end_time=timezone.now() + timedelta(minutes=survey.time_to_complete)
            )
            logger.debug(f"Попытка для результата теста создана: {survey_attempt}")

            result.attempts += 1
            result.score = 0
            result.status = 'assigned'
            logger.debug(f"Теперь использовано попыток: {result.attempts} из {survey.attempts}")
            result.save()

            question_sorting = []

            for survey_section in survey.survey_sections.all().order_by('item'):
                logger.debug(f"Отбор вопросов из раздела теста: {survey_section}")
                if survey_section.survey_section_questions.count() > survey_section.sample_size:
                    selected_survey_section_questions = survey_section.survey_section_questions.order_by('?')[:survey_section.sample_size]
                else:
                    selected_survey_section_questions = survey_section.survey_section_questions.order_by('?')
                logger.debug(f"Выбранные вопросы из раздела теста: {survey_section}")

                for selected_survey_section_question in selected_survey_section_questions:
                    logger.debug(f"Создание результата для вопроса теста: {selected_survey_section_question.question}")

                    question_sorting.append(selected_survey_section_question.question.id)

                    question_result = QuestionResult.objects.create(
                        survey_attempt=survey_attempt,
                        question=selected_survey_section_question.question,
                        status='assigned'
                    )
                    logger.debug(f"Результат для вопроса теста создан: {question_result}")

                    for answer in question_result.question.answers.all().order_by('item'):
                        logger.debug(f"Создание результата для ответа вопроса: {answer}")

                        answer_result = AnswerResult.objects.create(
                            question_result=question_result,
                            answer=answer,
                            status='assigned'
                        )
                        logger.debug(f"Результат для ответа вопроса создан: {answer_result}")

            logger.debug(f"Сортировка вопросов: {question_sorting}")
            if survey.random_questions:
                random.shuffle(question_sorting)
                logger.debug(f"Сортировка вопросов изменена: {question_sorting}")
            survey_attempt.question_sorting = json.dumps(question_sorting)
            survey_attempt.save()
            logger.debug(f"Сортировка вопросов записана: {question_sorting}")
        else:
            survey_attempt = last_attempt
            logger.debug(f"Попытка для результата теста получена: {survey_attempt}")

        if request.method == 'GET':
            serializer = SurveyAttemptSerializer(survey_attempt, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при получении попытки теста ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def survey_attempt_open(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        survey = task.survey
        result = task.survey_result

        executor = result.task.executor == request.user

        if not executor:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        last_attempt = result.survey_attempts.lasurvey('id') if result.survey_attempts.exists() else None
        logger.debug(f"Последняя попытка прохождения теста: {last_attempt}")

        if not last_attempt:
            logger.debug(f"Создание попытки для результата теста: {result}")

            if not survey.survey_sections.exists():
                return Response({"error": "Нет разделов в тесте"}, status=403)
            if not SurveySectionQuestion.objects.filter(survey_section__in=survey.survey_sections.all()).exists():
                return Response({"error": "В разделах нет вопросов"}, status=403)

            survey_attempt = SurveyAttempt.objects.create(
                survey_result=result,
                number = result.survey_attempts.count() + 1,
                status='assigned',
                start_time=timezone.now(),
                plan_end_time=timezone.now() + timedelta(minutes=survey.time_to_complete)
            )
            logger.debug(f"Попытка для результата теста создана: {survey_attempt}")

            result.attempts += 1
            result.score = 0
            result.status = 'assigned'
            logger.debug(f"Теперь использовано попыток: {result.attempts} из {survey.attempts}")
            result.save()

            question_sorting = []

            for survey_section in survey.survey_sections.all().order_by('item'):
                logger.debug(f"Отбор вопросов из раздела теста: {survey_section}")
                if survey_section.survey_section_questions.count() > survey_section.sample_size:
                    selected_survey_section_questions = survey_section.survey_section_questions.order_by('?')[:survey_section.sample_size]
                else:
                    selected_survey_section_questions = survey_section.survey_section_questions.order_by('?')
                logger.debug(f"Выбранные вопросы из раздела теста: {survey_section}")

                for selected_survey_section_question in selected_survey_section_questions:
                    logger.debug(f"Создание результата для вопроса теста: {selected_survey_section_question.question}")

                    question_sorting.append(selected_survey_section_question.question.id)

                    question_result = QuestionResult.objects.create(
                        survey_attempt=survey_attempt,
                        question=selected_survey_section_question.question,
                        status='assigned'
                    )
                    logger.debug(f"Результат для вопроса теста создан: {question_result}")

                    for answer in question_result.question.answers.all().order_by('item'):
                        logger.debug(f"Создание результата для ответа вопроса: {answer}")

                        answer_result = AnswerResult.objects.create(
                            question_result=question_result,
                            answer=answer,
                            status='assigned'
                        )
                        logger.debug(f"Результат для ответа вопроса создан: {answer_result}")

            logger.debug(f"Сортировка вопросов: {question_sorting}")
            if survey.random_questions:
                random.shuffle(question_sorting)
                logger.debug(f"Сортировка вопросов изменена: {question_sorting}")
            survey_attempt.question_sorting = json.dumps(question_sorting)
            survey_attempt.save()
            logger.debug(f"Сортировка вопросов записана: {question_sorting}")
        else:
            survey_attempt = last_attempt
            logger.debug(f"Попытка для результата теста получена: {survey_attempt}")

        if request.method == 'GET':
            serializer = SurveyAttemptSerializer(survey_attempt, context={'request': request})
            return Response(serializer.data)

    except Exception as e:
        logger.exception(f"Ошибка при получении попытки теста ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def survey_attempt_create(request, task_id):
    try:

        task = get_object_or_404(Task, pk=task_id)
        survey = task.survey
        result = task.survey_result

        executor = result.task.executor == request.user

        if not executor:
            return Response({"error": "Нет прав на результат задачи"}, status=403)

        attempt_available = survey.attempts > result.attempts
        logger.debug(f"Использовано попыток: {result.attempts} из {survey.attempts}. Есть еще попытки: {attempt_available}")

        last_attempt = result.survey_attempts.lasurvey('id') if result.survey_attempts.exists() else None
        logger.debug(f"Последняя попытка прохождения теста: {last_attempt}")

        last_attempt_end = last_attempt.end_time if last_attempt else None
        logger.debug(f"Последняя попытка прохождения теста завершена: {last_attempt_end}")

        need_create_attempt = last_attempt and last_attempt_end and attempt_available
        logger.debug(f"Необходимо создать попытку: {need_create_attempt}")

        if need_create_attempt:
            logger.debug(f"Создание попытки для результата теста: {result}")

            if not survey.survey_sections.exists():
                return Response({"error": "Нет разделов в тесте"}, status=403)
            if not SurveySectionQuestion.objects.filter(survey_section__in=survey.survey_sections.all()).exists():
                return Response({"error": "В разделах нет вопросов"}, status=403)

            survey_attempt = SurveyAttempt.objects.create(
                survey_result=result,
                number = result.survey_attempts.count() + 1,
                status='assigned',
                start_time=timezone.now(),
                plan_end_time=timezone.now() + timedelta(minutes=survey.time_to_complete)
            )
            logger.debug(f"Попытка для результата теста создана: {survey_attempt}")

            result.attempts += 1
            result.score = 0
            result.status = 'assigned'
            logger.debug(f"Теперь использовано попыток: {result.attempts} из {survey.attempts}")
            result.save()

            question_sorting = []

            for survey_section in survey.survey_sections.all().order_by('item'):
                logger.debug(f"Отбор вопросов из раздела теста: {survey_section}")
                if survey_section.survey_section_questions.count() > survey_section.sample_size:
                    selected_survey_section_questions = survey_section.survey_section_questions.order_by('?')[:survey_section.sample_size]
                else:
                    selected_survey_section_questions = survey_section.survey_section_questions.order_by('?')
                logger.debug(f"Выбранные вопросы из раздела теста: {survey_section}")

                for selected_survey_section_question in selected_survey_section_questions:
                    logger.debug(f"Создание результата для вопроса теста: {selected_survey_section_question.question}")

                    question_sorting.append(selected_survey_section_question.question.id)

                    question_result = QuestionResult.objects.create(
                        survey_attempt=survey_attempt,
                        question=selected_survey_section_question.question,
                        status='assigned'
                    )
                    logger.debug(f"Результат для вопроса теста создан: {question_result}")

                    for answer in question_result.question.answers.all().order_by('item'):
                        logger.debug(f"Создание результата для ответа вопроса: {answer}")

                        answer_result = AnswerResult.objects.create(
                            question_result=question_result,
                            answer=answer,
                            status='assigned'
                        )
                        logger.debug(f"Результат для ответа вопроса создан: {answer_result}")

            logger.debug(f"Сортировка вопросов: {question_sorting}")
            if survey.random_questions:
                random.shuffle(question_sorting)
                logger.debug(f"Сортировка вопросов изменена: {question_sorting}")
            survey_attempt.question_sorting = json.dumps(question_sorting)
            survey_attempt.save()
            logger.debug(f"Сортировка вопросов записана: {question_sorting}")

            if request.method == 'POST':
                serializer = SurveyAttemptSerializer(survey_attempt, context={'request': request})
                return Response(serializer.data)

        else:
            logger.debug(f"Нельзя создать попытку прохождения теста")
            return Response({"error": "Нельзя создать попытку прохождения теста"}, status=403)

    except Exception as e:
        logger.exception(f"Ошибка при получении попытки теста ID={task_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['PATCH'])
@permission_classes([AllowAny])
def send_answers(request, question_result_id):

    # Выводим отладочную информацию о запросе.
    logger.info(f'Ответ на вопрос: {request}, {request.body}')

    # Проверка корректности метода.
    if request.method != 'PATCH':
        return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=405)

    # Ловим ошибки.
    try:

        question_result = get_object_or_404(QuestionResult, pk=question_result_id)
        logger.debug(f"Результат вопроса: {question_result}")
        survey_attempt = question_result.survey_attempt
        logger.debug(f"Попытка теста: {survey_attempt}")
        survey_result = survey_attempt.survey_result
        logger.debug(f"Результат теста: {survey_result}")
        task = survey_result.task
        logger.debug(f"Задача: {survey_result}")

        executor = task.executor == request.user
        if not executor:
            return Response({"error": "Это тест для другого пользователя"}, status=403)
        logger.debug(f"Тест принадлежит пользователю")

        survey_finished = survey_result.finished
        if survey_finished:
            return Response({"error": "Тест уже завершен"}, status=403)
        logger.debug(f"Тест активен")

        attempt_time_out = survey_attempt.plan_end_time and timezone.now() > survey_attempt.plan_end_time
        if attempt_time_out:
            return Response(
                {
                    "error": "Время на попытку истекло",
                    "survey_attempt_status": survey_attempt.status,
                },
                status=403
            )
        logger.debug(f"Время на попытку еще есть")

        if survey_attempt.status == 'assigned':
            survey_attempt.status = 'in_progress'
            logger.debug(f"Попытка начата")

        question_result_finished = question_result.status in ['completed', 'failed']
        if question_result_finished:
            return Response(
                {
                    "error": "Вопрос завершен",
                    "survey_attempt_status": question_result.status,
                },
                status=403
            )
        logger.debug(f"Вопрос активен")

        # Разджисониваем.
        data = json.loads(request.body)
        logger.debug(f'Данные запроса на запись данных: {data}')

        answers = data.get("answer_results", [])
        for answer in answers:
            answer_result_id = answer.get("id")
            selected_answer = answer.get("selected_answer")
            selected_position = answer.get("selected_position")
            selected_text_input = answer.get("selected_text_input")
            selected_numeric_input = answer.get("selected_numeric_input")
            selected_relevant_point = answer.get("selected_relevant_point")

            answer_result = get_object_or_404(AnswerResult, pk=answer_result_id)
            logger.debug(f"Результат ответа до обработки: {answer_result}")

            if answer_result.answer.question.question_type == 'single_selection' or answer_result.answer.question.question_type == 'multiple_choice':
                answer_result.selected_answer = selected_answer
                correct_answer = answer_result.selected_answer == answer_result.answer.correct_answer
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'sorting':
                answer_result.selected_position = selected_position
                correct_answer = answer_result.selected_position == answer_result.answer.correct_item
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'compliance':
                answer_result.selected_relevant_point = get_object_or_404(RelevantPoint, pk=selected_relevant_point)
                correct_answer = answer_result.selected_relevant_point == answer_result.answer.relevant_point
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'text_input':
                answer_result.selected_text_input = selected_text_input
                correct_answer = answer_result.selected_text_input == answer_result.answer.correct_text_input
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'

            if answer_result.answer.question.question_type == 'numeric_input':
                answer_result.selected_numeric_input = selected_numeric_input
                correct_answer = answer_result.selected_numeric_input == answer_result.answer.correct_numeric_input
                if correct_answer:
                    logger.debug(f"Ответ верный")
                    answer_result.status = 'completed'
                else:
                    logger.debug(f"Ответ неверный")
                    answer_result.status = 'failed'
            if correct_answer:
                answer_result.score = answer_result.answer.score
            else:
                answer_result.score = 0
            answer_result.end_time = timezone.now()
            answer_result.save()
            logger.debug(f"Результат ответа после обработки: {answer_result}")

        correct_question = all(
            answer.status == 'completed'
            for answer in question_result.answer_results.all()
        )
        if correct_question:
            logger.debug(f"Все ответы на вопрос верные")
            question_result.status = 'completed'
            question_result.score = question_result.question.score
        else:
            logger.debug(f"Ответ неверный")
            question_result.status = 'failed'
            question_result.score = 0


        question_result.end_time = timezone.now()
        question_result.save()
        logger.debug(f"Результат вопроса после обработки: {question_result}")

        answers_scores_sum = question_result.answer_results.aggregate(sum=Sum('score'))['sum']
        logger.debug(f"Сумма баллов за ответы: {answers_scores_sum}")
        logger.debug(f"Баллы за вопрос: {question_result.score}")
        logger.debug(f"Текущие баллы за попытку: {survey_attempt.score}")
        survey_attempt.score += (answers_scores_sum + question_result.score)
        survey_attempt.save()
        logger.debug(f"Новые баллы за попытку: {survey_attempt.score}")
        survey_result.score += (answers_scores_sum + question_result.score)
        survey_result.save()
        logger.debug(f"Новые баллы за тест: {survey_result.score}")

        attempt_question_out = not survey_attempt.question_results.exclude(Q(status='completed') | Q(status='failed')).exists()
        logger.debug(f"Вопросы закончились: {attempt_question_out}")

        if (attempt_time_out or attempt_question_out) and not survey_attempt.end_time:

            if survey_attempt.status not in ['completed', 'failed', 'canceled']:
                logger.debug(f"Попытка еще не завершена")

                survey_attempt_completed = survey_attempt.score >= survey_result.task.survey.passing_score
                if survey_attempt_completed:
                    logger.debug(f"Тест пройден. Требуется: {survey_result.task.survey.passing_score} баллов. Набрано: {survey_attempt.score} баллов.")
                    survey_attempt.status = 'completed'
                    survey_result.status = 'completed'
                else:
                    logger.debug(f"Тест провален. Требуется: {survey_result.task.survey.passing_score} баллов. Набрано: {survey_attempt.score} баллов.")
                    survey_attempt.status = 'failed'
                    survey_result.status = 'failed'

                survey_finished = survey_result.attempts >= survey_result.task.survey.attempts
                if survey_finished:
                    survey_result.finished = True

                survey_attempt.end_time = timezone.now()
                survey_attempt.save()
                survey_result.end_time = timezone.now()
                survey_result.save()
                logger.debug(f"Обновленный результат попытки: {survey_attempt}")
                logger.debug(f"Обновленный результат теста: {survey_result}")

                for question_result in survey_attempt.question_results.all():
                    if question_result.status not in ['completed', 'failed']:
                        logger.debug(f"Вопрос не завершен при завершении попытки: {question_result}")
                        question_result.status = 'failed'
                        question_result.save()
                        logger.debug(f"Вопрос завершен: {question_result}")
            else:
                logger.debug(f"Попытка уже завершена")

        # Возвращаем успешный JSON-ответ с информацией о процессе инициализации.
        attempt_finished = survey_attempt.status in ['completed', 'failed']
        if attempt_finished:
            serializer = SurveyAttemptSerializer(survey_attempt, context={'request': request})
            return Response({
                'status': 'ok',
                'type': 'survey_attempt',  # можно пометить, что это полный результат
                'data': serializer.data
            })
        else:
            serializer = QuestionResultSerializer(question_result, context={'request': request})
            return Response({
                'status': 'ok',
                'type': 'question_result',  # пометка, что это частичный ответ
                'data': serializer.data
            })

    except Exception as e:
        logger.exception(f"Ошибка при отправке ответов на вопрос ID={question_result_id}")
        return Response({"error": "Ошибка сервера", "details": str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def survey_finish(request, survey_attempt_id):

    # Выводим отладочную информацию о запросе.
    logger.info(f'Завершение теста: {request}, {request.body}')

    # Проверка корректности метода.
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Неверный метод'}, status=405)

    # Ловим ошибки.
    try:

        survey_attempt = get_object_or_404(SurveyAttempt, pk=survey_attempt_id)
        logger.debug(f"Попытка теста: {survey_attempt}")
        survey_result = survey_attempt.survey_result
        logger.debug(f"Результат теста: {survey_result}")
        task = survey_result.task
        logger.debug(f"Задача: {survey_result}")

        executor = task.executor == request.user
        if not executor:
            return Response({"error": "Это тест для другого пользователя"}, status=403)
        logger.debug(f"Тест принадлежит пользователю")

        survey_finished = survey_result.finished
        if survey_finished:
            return Response({"error": "Тест уже завершен"}, status=403)
        logger.debug(f"Тест активен")

        attempt_finished = survey_attempt.status in ['completed', 'failed']
        logger.debug(f"Попытка завершена: {attempt_finished }")
        survey_attempt_completed = survey_attempt.score >= survey_result.task.survey.passing_score
        logger.debug(f"Попытка успешна: {survey_attempt_completed}")
        if survey_attempt_completed:
            logger.debug(f"Тест пройден. Требуется: {survey_result.task.survey.passing_score} баллов. Набрано: {survey_attempt.score} баллов.")
            if not attempt_finished:
                survey_attempt.status = 'completed'
            survey_result.status = 'completed'
        else:
            logger.debug(f"Тест провален. Требуется: {survey_result.task.survey.passing_score} баллов. Набрано: {survey_attempt.score} баллов.")
            if not attempt_finished:
                survey_attempt.status = 'failed'
            survey_result.status = 'failed'

        if not attempt_finished:
            survey_attempt.end_time = timezone.now()
            survey_attempt.save()
            logger.debug(f"Обновленный результат попытки: {survey_attempt}")

        survey_finished = survey_result.attempts >= survey_result.task.survey.attempts
        if survey_finished:
            survey_result.finished = True
        survey_result.end_time = timezone.now()
        survey_result.save()

        for question_result in survey_attempt.question_results.all():
            if question_result.status not in ['completed', 'failed']:
                logger.debug(f"Вопрос не завершен при завершении попытки: {question_result}")
                question_result.status = 'failed'
                question_result.save()
                logger.debug(f"Вопрос завершен: {question_result}")

        logger.debug(f"Обновленный результат теста: {survey_result}")

        serializer = SurveyAttemptSerializer(survey_attempt, context={'request': request})
        return Response({
            'status': 'ok',
            'data': serializer.data
        })

    # Ловим ошибки декодирования JSON.
    except json.JSONDecodeError as e:
        logger.info(f'Ошибка декодирования JSON при завершении теста: {e}')
        return Response({'status': 'error', 'message': 'Невалидный JSON'}, status=400)

    # Обрабатываем другие исключения, выводим ошибку.
    except Exception as e:
        logger.info(f'Error in scorm_initialize: {e}')
        return Response({'status': 'error', 'message': 'Неизвестная ошибка сервера'}, status=500)
